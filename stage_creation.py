import pygame
from scipy.spatial import Delaunay
import numpy as np
import random


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

    # coordenadas de posición de la room
    def coord(self,x,y):
        self.x = x
        self.y = y
        self.centerx = x + self.width/2
        self.centery = y + self.length/2

    # check para asegurarse de que las rooms no sean colocadas una encima de otra
    def isColliding(self,room):
        # Para saber si 2 cuadrados están intersectándose, sus proyecciones en cada dimensión tienen que estar
        # intersectándose (rangos x e y)
        return (self.x + self.width  >= room.x and self.x <= room.x + room.width ) and (
                self.y + self.length  >= room.y and self.y <= room.y + room.length)


# genera la room
def generateRoom(size):
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

# Genera arreglo de 0's primeramente
# Después agrega las salas de forma iterativa (el límite de salas aún no esta definido)
# 
def initGrid(size):
    #Inicialización de grid tamaño size x size llena de 0's
    grid = []
    for i in range(size):
        row = [0] * size
        grid.append(row)
        
    # Creación de salas
    # Generacion y checkeo de que las salas no esten chocando
    rooms = []
    for k in range(200):
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
                grid[i][j] = 1
        rooms.append(g)
    # Crear el grafo mediante la triangulación de Delaunay
    centers = np.empty([len(rooms),2])
    for i in range(len(rooms)):
        centers[i,0] = rooms[i].centerx
        centers[i,1] = rooms[i].centery

    triangles = centers[Delaunay(centers).simplices]
    return grid,rooms,triangles

def printGrid(grid):
    for j in range(len(grid)):
        for i in range(len(grid)):
            if(grid[i][j] != 0):
                print(chr(grid[i][j]), end=" ")
            else:
                print(" ", end=" ")
        print()

def stage_creation(rows):
    grid,rooms,triangles = initGrid(rows)
    printGrid(grid)
    return grid,rooms,triangles

def drawGrid(window, size, rows, grid, rooms, triangles):
    blockSize = size / rows
    for i in range(rows):
        for j in range(rows):
            rect = pygame.Rect(i*blockSize+0.5, j*blockSize+0.5, blockSize-1, blockSize-1)
            if grid[i][j] == 1:
                pygame.draw.rect(window, (3, 88, 140), rect)
            else:
                pygame.draw.rect(window, (1, 13, 38), rect)
    for r in rooms:
        pygame.draw.circle(window, (105, 158, 191), (r.centerx*blockSize, r.centery*blockSize), 5)    
    for t in triangles:
        p = t*blockSize
        pygame.draw.polygon(window, (3, 140, 127), points=p, width=2)

def redraw(window,size,rows,grid,rooms, triangles):
    window.fill((0, 3, 13))
    drawGrid(window,size,rows,grid,rooms, triangles)

    pygame.display.update()

def main():
    size = 1000
    rows = 50
    grid,rooms,triangles = stage_creation(rows)

    window = pygame.display.set_mode((size,size),pygame.RESIZABLE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                size = event.h
                window = pygame.display.set_mode((event.h, event.h),
                                              pygame.RESIZABLE)
        redraw(window,size,rows,grid,rooms,triangles)

main()
