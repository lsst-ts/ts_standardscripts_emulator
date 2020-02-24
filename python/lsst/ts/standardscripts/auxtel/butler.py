"""Fake up the butler too, always returning a rather boring image"""

import numpy as np
import lsst.afw.image as afwImage

class Butler():
    def __init__(self, root):
        self.root = root
        pass
    
    def datasetExists(self, dataType, dataId, **kwargs):
        return True
    
    def get(self, dataType, dataId, **kwargs):
        exp = afwImage.ExposureF(4036, 4000)
        cen = 2500, 2300
        exp.image.array[cen[0] - 10: cen[0] + 10, cen[1] - 10: cen[1] + 15] = 2000
        exp.image.array[cen[0], cen[1]] = 3000
        
        return exp
