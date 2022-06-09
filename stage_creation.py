
import random
import pygame



def a_estrellita(graph, start, end):
    
    return 0

# generar una room de forma random,
# no debe ser mas grande ni identica que la gridP principal,
# que escale con la grid principal
# (si se cambia la escala de la gridP que las rooms generadas escalen con ellas)
# el como sean definidas las piezas sera clave para entregarle coherencia a las rooms
# restricciones:
    # una room no puede ser mas grande que su area total (sizeXsize)/[valor random]
    # una room no puede ser mas larga que (sizeXsize)/[valor random]*1/3
    # su grosor minimo no puede ser menor a 3
class room:
    def __init__(self,length,width):
        self.length = length
        self.width = width

    # coordenadas de posicion de la room
    def coord(self,x,y):
        self.x = x
        self.y = y

    # check para asegurarse de que las rooms no sean colocadas una ensima de otra
    def isColliding(self,room):
        #Para saber si 2 cuadrados están intersectándose, sus proyecciones en cada dimensión tienen que estar
        #intersectándose (rangos x e y)
        return (self.x + self.width  >= room.x and self.x <= room.x + room.width ) and (
                self.y + self.length  >= room.y and self.y <= room.y + room.length)


# genera la 
def generateRoom(size):
    totalArea = size*size
    maxRoomA = int(totalArea/20) #Area maxima de una sala
    maxL = int(maxRoomA / 3) #Largo maximo de una sala
    if(maxL > size/3):
        maxL = int(size/3)
    length =  random.randint(3,maxL)
    maxW = int(maxRoomA/length)
    if(maxW > size/3):
        maxW = int(size/3)
    width = random.randint(3,maxW)
    r = room(length,width)
    print("Debug:" + str(length) + "," + str(width))
    #Definición de coordenadas
    coordx = random.randint(0,size-width)
    coordy = random.randint(0,size-length)
    r.coord(coordx,coordy)
    #Maximo posicioen es size-width
    return r

# genera arreglo de 0's primeramente
# despues agrega las salas de forma iterativa (el limite de salas aun no esta definido)
# 
def initGrid(size):
    #Inicialización de grid tamaño size x size llena de 0's
    grid = []
    for i in range(size):
        row = [0] * size
        grid.append(row)
        
    #Creación de salas
    #Generacion y checkeo de que las salas no esten chocando
    rooms = []
    for k in range(20):
        g = generateRoom(size)
        #Checkeo de colisión entre salas
        for r in rooms:
            if g.isColliding(r):
                g = None
                break
        if g == None:
            continue
        for i in range(g.x, g.x+g.width):
            for j in range(g.y, g.y+g.length):
                grid[i][j] = ord('A') + k
        rooms.append(g)
    return grid

def printGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if(grid[i][j] != 0):
                print(chr(grid[i][j]), end=" ")
            else:
                print(" ", end=" ")
        print()


# main
grid = initGrid(50)
printGrid(grid)

