"""Totally fake the SAL CSC system"""

__all__ = ["CSC", "CSC_Cmd", "CSC_Evt"]

class CSC:
    """A Commandable Sal Component"""    
    def __init__(self):
        pass

class CSC_Cmd:
    """A command supported by a CSC

    I'm not sure if all or any of these methods are really
    in the base class (some almost certainly aren't), but
    it doesn't matter here
    """
    def __init__(self):
        pass

    async def start(self):
        pass

class CSC_Evt:
    """An event associated with a CSC

    I'm not sure if all or any of these methods are really
    in the base class (some almost certainly aren't), but
    it doesn't matter here
    """
    def __init__(self):
        pass

    async def flush(self):
        pass

    async def next(self, flush=False, timeout=0):
        return self

