"""Fake up the butler too, always returning a rather boring image"""

import numpy as np
import lsst.daf.base as dafBase
import lsst.afw.image as afwImage

class Butler():
    def __init__(self, root):
        self.root = root
        pass
    
    def datasetExists(self, dataType, dataId, **kwargs):
        return True
    
    def get(self, dataType, dataId, **kwargs):
        nx, ny = 4036, 4000
        exp = afwImage.ExposureF(nx, ny)
        exp.image.array = np.random.normal(size=nx*ny).astype(np.float32).reshape(ny, nx)

        md = dafBase.PropertyList()
        md.set("OBJECT", "unknown")
        exp.setMetadata(md)
        
        cen = 2500, 2300
        exp.image.array[cen[0] - 10: cen[0] + 10, cen[1] - 10: cen[1] + 15] = 2000
        exp.image.array[cen[0], cen[1]] = 3000
        
        return exp
