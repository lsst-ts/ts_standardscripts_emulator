"""A simulator for the LATISS instrument on auxTel"""

import asyncio
from .csc import *


class ATArchiver(CSC):
    """The auxTel Archiver component"""

    class ImageInOODS(CSC_Evt):
        def __init__(self):
            super().__init__()

        async def next(self, flush=False, timeout=0):
            super().next(flush, timeout)
            self.obsid = f"AT_O_{ATCamera.dayObs}_{ATCamera.seqNum}"

            return self
    
    def __init__(self):
        super().__init__()

        self.evt_imageInOODS = ATArchiver.ImageInOODS()

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class ATCamera(CSC):
    """The auxTel Camera component"""
    
    # important if you're reading back real data
    dayObs = None
    seqNum = None

    def __init__(self, dayObs, seqNum):
        super().__init__()

        ATCamera.dayObs = dayObs
        ATCamera.seqNum = seqNum

    async def expose(self, exptime):
        if LATISS.domain.verbose:
            print(f"exposing {exptime} second{'' if exptime == 1 else 's'}"
                  f" ({ATSpectrograph.filter} {ATSpectrograph.grating})")

        await asyncio.sleep(exptime*LATISS.domain.time_per_second)
        ATCamera.seqNum += 1

        if LATISS.domain.verbose:
            print(f"exposure finished")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class ATSpectrograph(CSC):
    """The auxTel Spectrograph component"""

    grating = None
    filter = None

    class ReportedFilterPosition(CSC_Evt):
        """Return a struct including the filter name"""
        def __init__(self):
            super().__init__()

        async def aget(self):
            self.name = ATSpectrograph.filter
            return self

    class ReportedDisperserPosition(CSC_Evt):
        """Return a struct including the grating name"""
        def __init__(self):
            super().__init__()

        async def aget(self):
            self.name = ATSpectrograph.grating
            return self

    def __init__(self,  grating, filter):
        super().__init__()

        ATSpectrograph.grating = grating
        ATSpectrograph.filter = filter
        
        self.evt_reportedFilterPosition = ATSpectrograph.ReportedFilterPosition()
        self.evt_reportedDisperserPosition = ATSpectrograph.ReportedDisperserPosition()

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class LATISS:
    """The LATISS instrument"""

    domain = None

    def __init__(self, domain, dayObs="2020-02-20", seqNum=0):
        LATISS.domain = domain

        self.atarchiver = ATArchiver()
        self.atcamera = ATCamera(dayObs=dayObs, seqNum=seqNum)
        self.atspectrograph = ATSpectrograph(None, None)

    async def setup_atspec(self, grating, filter):
        if grating is not None:
            ATSpectrograph.grating = grating
        if filter is not None:
            ATSpectrograph.filter = filter

    async def take_object(self, exptime, n, grating=None, filter=None):
        await self.setup_atspec(grating, filter)

        for i in range(n):
            await self.atcamera.expose(exptime)

