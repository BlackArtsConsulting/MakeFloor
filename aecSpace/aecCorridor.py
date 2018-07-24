import traceback

from aecSpace.aecGeometry import aecGeometry
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer

class aecCorridor():
    """
    Represents architectural corridors of various configurations.
    """
    __dimensionError = "Critical corridor dimension exceeds floor boundary."
    __minPersons = 3
    __minWidth = 1700
    __personWidth = 570
    __geometry = aecGeometry()
    __shaper = aecShaper() 
    __spacer = aecSpacer()
    
    # Defines a series of constants indicating corridor types.
    
    Cross, Equatorial, H, L, Polar, T, U = range(0, 7)
    
    __slots__ = \
    [
        '__corridor',
        '__persons',
        '__space',
        '__width'
    ]   
    
    def __init__(self, corridor: int = 1,
                       origin: aecPoint = aecPoint(),
                       xSize: float = 1700, 
                       ySize: float = 1700, 
                       persons: int = 3):
        """
        Constructor by default creates an Equatorial corridor.       
        """
        self.__corridor = self.Equatorial
        self.__persons = self.__minPersons
        self.__width = self.__minWidth
        if persons > 3: 
            self.__persons = persons = int(persons)
            persons -= self.__minPersons
            self.__width += (persons * self.__minWidth)
        self.__space = aecSpace()

    @property
    def persons(self) -> int:
        """
        Returns the capacity of the corridor as the quantity of 
        persons who can pass along its length simultaneously.
        Returns None on failure.
        """
        try:
            return self.__passage
        except Exception:
            traceback.print_exc() 
            return None
        
    @persons.setter
    def persons(self, value: int = 3) -> int:
        """
        Sets the capacity of the corridor as the quantity of 
        persons who can pass along its length simultaneously.
        Returns None on failure.
        """
        try:
            value = abs(int(value))
            if value < self.__minPersons: value = self.__minPersons
            self.__persons = value
            if value > self.__minPersons: value -= self.__minPersons
            self.__width = self.__minWidth + (self.__personWidth * value)
        except Exception:
            traceback.print_exc() 
            
    @property
    def space(self) -> aecSpace:
        """
        Returns the aecSpace object.
        Returns None on failure.
        """
        try:
            return self.__space
        except Exception:
            traceback.print_exc() 
            return None
        
    @property
    def width(self) -> float:
        """
        Returns the corridor width.
        Returns None on failure.
        """
        try:
            return self.__width
        except Exception:
            traceback.print_exc() 
            return None        

    def makeCross(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to a cross shape within the
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if self.width >= floor.size_x or \
               self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeCross(origin = origin,
                                             xSize = xSize,
                                             ySize = ySize,
                                             xWidth = self.width,
                                             yDepth = self.width)
            if not points: raise Exception
            self.space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)
        except ValueError:
            print(self.__dimensionError)
            return False        
        except Exception:
            traceback.print_exc() 
            return False        

    def makeEquatorial(self, floor: aecSpace, 
                             marginWest: float = 0.0,
                             marginEast: float = 0.0,
                             rotate: float = 0.0) -> bool:
        """
        Sets the corridor to an vertically centered box shape within
        the specified margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + marginWest
            yPnt = self.__geometry.getMidpoint(floorBox.SW, floorBox.NW).y - (self.__width * 0.5)
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - marginEast) - xPnt)
            points = self.__shaper.makeBox(origin = origin, 
                                           xSize = xSize, 
                                           ySize = self.width)
            if not points: raise Exception
            self.space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)    
        except ValueError:
            print(self.__dimensionError)
            return False     
        except Exception:
            traceback.print_exc() 
            return False        
               
    def makeH(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to an H shape within the specified
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if (self.width * 2) >= floor.size_x or \
                self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeH(origin = origin,
                                         xSize = xSize,
                                         ySize = ySize,
                                         xWidth1 = self.width,
                                         xWidth2 = self.width,
                                         yDepth = self.width)
            if not points: raise Exception
            self.__space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)                
        except ValueError:
            print(self.__dimensionError)
            return False        
        except Exception:
            traceback.print_exc() 
            return False
        
    def makeL(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to an L shape within the specified
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if self.width >= floor.size_x or \
               self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeL(origin = origin,
                                         xSize = xSize,
                                         ySize = ySize,
                                         xWidth = self.width,
                                         yDepth = self.width)
            if not points: raise Exception
            self.__space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)            
        except ValueError:
            print(self.__dimensionError)
            return False
        except Exception:
            traceback.print_exc() 
            return False        
        
    def makePolar(self, floor: aecSpace, 
                        roomsWest: int = 2,
                        roomsEast: int = 2,
                        roomsNorth: int = 0,
                        roomsNorthSize: float = 3000,
                        roomsSouth: int = 0,
                        roomsSouthSize: float = 3000) -> bool:
        """
        Sets the corridor to a horizontally centered box shape within
        the specified margin of the delivered floor's bounding box.
        Populates the perimeter of the cooridor with the specified
        number of rooms in each compass quadrant and returns the 
        list of room spaces in anticlockwise order, starting either
        from the southwestern room (if it exists) or the southeastern room.
        Returns None on Failure.
        """
        try:
            if self.width >= floor.size_x: raise ValueError
            roomsWest = abs(int(roomsWest))
            roomsEast = abs(int(roomsEast))
            if roomsWest < 1: roomsWest = 1
            if roomsEast < 1: roomsEast = 1
            roomsNorth = abs(int(roomsNorth))
            roomsSouth = abs(int(roomsSouth))
            if roomsNorth <= 0: 
                roomsNorth = 0
                roomsNorthSize = 0
            if roomsSouth <= 0: 
                roomsSouth = 0
                roomsSouthSize = 0
            if roomsNorth > 2: roomsNorth = 2
            if roomsSouth > 2: roomsSouth = 2   
            if roomsNorth > 0 and roomsNorthSize < 1000: roomsNorthSize = 1000
            if roomsSouth > 0 and roomsSouthSize < 1000: roomsSouthSize = 1000
            if floor.size_y <= (roomsNorthSize + roomsSouthSize): raise ValueError
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = self.__geometry.getMidpoint(floorBox.SW, floorBox.SE).x - (self.width * 0.5)
            yPnt = floorBox.SW.y
            if roomsSouth: yPnt += roomsSouthSize
            origin = aecPoint(xPnt, yPnt)
            if roomsNorth > 0: ySize = abs((floorBox.NW.y - roomsNorthSize) - yPnt)
            else: ySize = abs(floorBox.NW.y - yPnt)
            points = self.__shaper.makeBox(origin = origin, 
                                           xSize = self.width, 
                                           ySize = ySize)
            if not points: raise Exception
            self.space.boundary = points
            if not self.space.fitWithin(floor.points_floor): return False       
            xRoom = abs(origin.x - floorBox.SW.x)
            yRoom = ySize / roomsWest
            xPnt = floorBox.SW.x
            yPnt = origin.y
            oRoom = aecPoint(xPnt, yPnt)
            points = self.__shaper.makeBox(origin = oRoom, 
                                           xSize = xRoom, 
                                           ySize = yRoom) 
            room = aecSpace()
            room.boundary = points
            westRooms = [room] + self.__spacer.place(room, roomsWest - 1, y = yRoom)
            westRooms.reverse()
            xRoom = abs(floorBox.SE.x - (origin.x + self.width))
            yRoom = ySize / roomsEast            
            xPnt = origin.x + self.width
            oRoom = aecPoint(xPnt, yPnt)
            points = self.__shaper.makeBox(origin = oRoom, 
                                           xSize = xRoom, 
                                           ySize = yRoom) 
            room = aecSpace()
            room.boundary = points
            eastRooms = [room] + self.__spacer.place(room, roomsEast - 1, y = yRoom)
            rooms = []
            if roomsNorth > 0:
                xPnt = floorBox.NW.x
                yPnt = floorBox.NW.y - roomsNorthSize
                oRoom = aecPoint(xPnt, yPnt)
                xRoom = abs(floorBox.NE.x - floorBox.NW.x)
                yRoom = roomsNorthSize
                if roomsNorth == 2: xRoom *= 0.5
                points = self.__shaper.makeBox(origin = oRoom, 
                                               xSize = xRoom, 
                                               ySize = yRoom)                 
                room = aecSpace()
                room.boundary = points
                northRooms = []
                northRooms.append(room)
                if roomsNorth == 2: 
                    northRooms.append(self.__spacer.copy(room, x = xRoom))
                    northRooms.reverse()
            if roomsSouth > 0:
                xPnt = floorBox.SW.x
                yPnt = floorBox.SW.y
                oRoom = aecPoint(xPnt, yPnt)
                xRoom = abs(floorBox.NE.x - floorBox.NW.x)
                yRoom = roomsSouthSize
                if roomsSouth == 2: xRoom *= 0.5
                points = self.__shaper.makeBox(origin = oRoom, 
                                               xSize = xRoom, 
                                               ySize = yRoom)                 
                room = aecSpace()
                room.boundary = points
                southRooms = []
                southRooms.append(room)
                if roomsSouth == 2: southRooms.append(self.__spacer.copy(room, x = xRoom))
                rooms = southRooms
            rooms += eastRooms
            if roomsNorth: rooms += northRooms
            rooms += westRooms
            for room in rooms: room.fitWithin(floor.points_floor)
            return rooms
        except ValueError:
            print(self.__dimensionError)
            return None
        except Exception:
            traceback.print_exc() 
            return None 
        
    def makeT(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to an T shape within the specified
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if self.width >= floor.size_x or \
               self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeT(origin = origin,
                                         xSize = xSize,
                                         ySize = ySize,
                                         xWidth = self.width,
                                         yDepth = self.width)
            if not points: raise Exception
            self.__space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)            
        except ValueError:
            print(self.__dimensionError)
            return False
        except Exception:
            traceback.print_exc() 
            return False                
           
    def makeU(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to a U shape within the specified
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if (self.width * 2) >= floor.size_x or \
                self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeU(origin = origin,
                                         xSize = xSize,
                                         ySize = ySize,
                                         xWidth1 = self.width,
                                         xWidth2 = self.width,
                                         yDepth = self.width)
            if not points: raise Exception
            self.__space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)                
        except ValueError:
            print(self.__dimensionError)
            return False
        except Exception:
            traceback.print_exc() 
            return False       
        
        
        
