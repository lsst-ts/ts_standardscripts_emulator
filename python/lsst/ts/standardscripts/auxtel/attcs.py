"""A simulator for the ATTCS instrument on auxTel"""

import asyncio
import numpy as np
from .csc import *

__all__ = ["ATCCS"]

#
# The positions of a few stars that we might observe
#
knownPositions = {
    "HD 185975" : (180, -60),   # near the south ecliptic pole
    "HD 146233" : (100, 30),    # I have no idea!
}


class Domain:
    """Really DDS internals, but I'm going to hijack it for simulator internals"""
    def __init__(self, time_per_second, verbose):
        self.time_per_second = time_per_second  # multiplier for times when emulating e.g. exposures
        self.verbose = verbose


class ApplyFocusOffset(CSC_Cmd):
    def __init__(self):
        super().__init__()

    async def set_start(self, offset):
        pass


class ATAOS(CSC):
    """The auxTel Active Optics System"""

    def __init__(self):
        super().__init__()

        self.cmd_applyFocusOffset = ApplyFocusOffset()


class ATPTG(CSC):
    """The auxTel PoinTnG component"""

    def __init__(self):
        super().__init__()

        self.cmd_pointNewFile = CSC_Cmd()
        self.cmd_pointAddData = CSC_Cmd()


class Hexapod(CSC):
    """The auxTel PoinTnG component"""
    def __init__(self):
        super().__init__()

        self.evt_positionUpdate = CSC_Evt()


class ATTCS:
    """The ATTCS instrument"""
    
    def __init__(self, time_per_second=0, verbose=False):
        self.domain = Domain(time_per_second, verbose)
        self.long_timeout = 0

        self.atptg = ATPTG()
        self.ataos = ATAOS()
        self.athexapod = Hexapod()

        self._name = None
        self._ra = 0
        self._dec = 0
        self._pa_ang = None
        self._slew_timeout = None

        self._dx = 0
        self._dy = 0

    async def offset_xy(self, dx, dy, persistent=False):
        offset_delay = 1

        if persistent:
            dx += self._dx
            dy += self._dy
        
        await asyncio.sleep(offset_delay*self.domain.time_per_second)

        self._dx = dx
        self._dy = dy

        return (dx, dy)
    

    async def slew_object(self, name, pa_ang=0, slew_timeout=0):
        self._name = name
        self._pa_ang = pa_ang
        self._slew_timeout = slew_timeout

        ra, dec = knownPositions.get(name, (0, 0))

        slew_time = 0.1*np.hypot(ra - self._ra, dec - self._dec)

        if self.domain.verbose:
            print(f"slewing to {name}: ({ra}, {dec})")

        await asyncio.sleep(slew_time*self.domain.time_per_second)
        self._ra, self._dec = ra, dec

        if self.domain.verbose:
            print(f"slew complete")

        return (self._ra, self._dec)
