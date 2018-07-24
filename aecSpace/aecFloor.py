import traceback

from aecSpace.aecCorridor import aecCorridor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup

class aecFloor():
    """
    Represents the spatial configuration of a single floor.
    """
    
    __shaper = aecShaper() 
    
    __slots__ = \
    [
        '__corridor',
        '__floor',
        '__rooms'
    ]   

    def __init__(self):
        self.__corridor = aecCorridor()
        self.__floor = aecSpace()
        self.__rooms = aecSpaceGroup()      
        points = self.__shaper.makeBox(xSize = 15000, ySize = 10000) 
        if points: 
            self.__floor.boundary = points
            self.__floor.height = 4000
            self.__floor.level = 0.0
            self.__corridor.space.height = 4000

    @property
    def corridor(self) -> aecSpace:
        """
        Returns the corridor space..
        Returns None on failure.
        """
        try:
            return self.__corridor
        except Exception:
            traceback.print_exc() 
            return None
               
    @property
    def floor(self) -> aecSpace:
        """
        Returns the floor space..
        Returns None on failure.
        """
        try:
            return self.__floor
        except Exception:
            traceback.print_exc() 
            return None
        
    @property
    def rooms(self) -> aecSpaceGroup:
        """
        Returns the spaceGroup containing all the occupiable spaces.
        Returns None on failure.
        """
        try:
            return self.__rooms
        except Exception:
            traceback.print_exc() 
            return None
        
        
    