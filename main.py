
import random

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
    def isColliding(room):
        return not (self.x >= room.x + room.length)



def generateRoom(size):
    totalArea = size*size
    maxRoomA = totalArea/16 #Area maxima de una sala
    maxL = maxRoomA / 3 #Largo maximo de una sala
    length =  random.randint(3,maxL)    
    maxW = maxRoomA/length
    width = random.randint(3,maxW)

    return room(length,width)

# genera arreglo de 0's primeramente
# despues agrega las salas de forma iterativa (el limite de salas aun no esta definido)
# 
def initGrid(size):
    grid = []
    for i in range(size):
        row = [0] * size
        grid.append(row)
        

def printGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            print(grid[i][j])



grid = initGrid(27)




# generador de rooms
#def room():
    
def a_estrellita(graph, start, end):
    
    return 0




