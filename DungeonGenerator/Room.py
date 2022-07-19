import random

class room:
    def __init__(self,length,width):
        self.length = length
        self.width = width
        self.entrances = set()
        self.mustBeEmpty = set()

    # coordenadas de posición de la room
    def coord(self,x,y):
        self.x = x
        self.y = y
        self.centerx = x + self.width/2
        self.centery = y + self.length/2
    
    # agrega una entrada a la habitacion
    def addEntrance(self, tileCoords):
        if tileCoords not in self.entrances:
            self.entrances.add(tileCoords)
    
    # retorna un set con todas las entradas de una habitacion
    def getEntrances(self):
        return self.entrances
    
    def addEmptyTile(self, tileCoords):
        self.mustBeEmpty.add(tileCoords)
    
    def getEmptyTiles(self):
        return self.mustBeEmpty
    
    

    # check para asegurarse de que las rooms no sean colocadas una encima de otra
    def isColliding(self,room):
        # Para saber si 2 cuadrados están intersectándose, sus proyecciones en cada dimensión tienen que estar
        # intersectándose (rangos x e y)
        return (self.x + self.width  >= room.x and self.x <= room.x + room.width ) and (
                self.y + self.length  >= room.y and self.y <= room.y + room.length)
    def isCollidingMany(self,rooms):
        for r in rooms:
            if self.isColliding(r):
                return True
    # genera la room
    @classmethod
    def generateRoom(self,size):
        totalArea = size*size
        maxRoomA = int(totalArea/20) # Área máxima de una sala
        maxL = int(maxRoomA / 3) # Largo máximo de una sala
        if(maxL > size/3):
            maxL = int(size/3)
        length =  random.randint(3,maxL)
        maxW = int(maxRoomA/length)
        if(maxW > size/3):
            maxW = int(size/3)
        width = random.randint(3,maxW)
        r = room(length,width)
        #print("Debug:" + str(length) + "," + str(width))
        # Definición de coordenadas
        coordx = random.randint(0,size-width)
        coordy = random.randint(0,size-length)
        r.coord(coordx,coordy)
        # Máximo posición es size-width
        return r