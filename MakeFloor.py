from random import randint

from hypar import glTF

from aecSpace.aecFloor import aecFloor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
    
model = glTF()
colorAqua = model.add_material(0.3, 0.72, 0.392, 0.8, 0.5, "Aqua")
colorBlue = model.add_material(0.0, 0.631, 0.945, 0.8, 0.5, "Blue")
colorCyan = model.add_material(0.275, 0.941, 0.941, 0.8, 0.5, "Cyan")
colorTeal = model.add_material(0.0, 0.51, 0.51, 0.8, 0.8, "Teal")
colorGreen = model.add_material(0.486, 0.733, 0.0, 0.8, 0.5, "Green")

def getColor(color: int = 0):
    if color == 0: return colorAqua
    if color == 1: return colorBlue
    if color == 2: return colorCyan
    if color == 3: return colorTeal

def makeFloor(roomsSouth: int = 1, 
              roomsEast: int = 2, 
              roomsNorth: int = 1, 
              roomsWest: int = 2,
              roomsNorthSize: float = 12000,
              roomsSouthSize: float = 15000):
    height = 3500
    shell = aecFloor()
    floor = shell.floor
    rooms = shell.rooms
    corridor = shell.corridor
    if roomsSouth == 0:
        if randint(0, 1) == 0: roomsNorth = 0
        corridor.persons = 10
    else: corridor.persons = 5
    roomsTotal = roomsSouth + roomsEast + roomsNorth + roomsWest    
    shaper = aecShaper()
    floorSizeX = 30000
    floorSizeY = 70000
    floor.boundary = shaper.makeBox(aecPoint(), floorSizeX, floorSizeY)
    rooms = corridor.makePolar(floor, 
                               roomsWest = roomsWest, 
                               roomsEast = roomsEast,
                               roomsNorth = roomsNorth,
                               roomsNorthSize = roomsNorthSize,
                               roomsSouth = roomsSouth, 
                               roomsSouthSize = roomsSouthSize) 
    corridor.space.height = height
    mesh = corridor.space.mesh_graphic
    model.add_triangle_mesh(mesh.vertices, mesh.normals, mesh.indices, colorGreen)    
    if roomsTotal > 8:
        join = randint(0, roomsTotal - 2)  
        if rooms[join].add(rooms[join + 1].points_floor): del rooms[join + 1]
    for room in rooms:
        room.height = height
        mesh = room.mesh_graphic
        model.add_triangle_mesh(mesh.vertices, mesh.normals, mesh.indices, getColor(randint(0, 3)))   
    return {"model": model.save_base64(), 'computed':{'Total rooms':roomsTotal}}   
#    model.save_glb('C:\\Users\\Anthony\\Dropbox\\Business\\BlackArts\\Development\\GitHub\\MakeFloor\\model.glb')
#
#
#makeFloor(roomsSouth = randint(1, 2), 
#          roomsEast = randint(1, 8), 
#          roomsNorth = randint(1, 2), 
#          roomsWest= randint(1, 8),
#          roomsNorthSize = randint(8000, 15000),
#          roomsSouthSize = randint(8000, 15000))
