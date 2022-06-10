import pygame
from scipy.spatial import Delaunay
import numpy as np
from stage_models import room
from draw_handler import redraw

def a_estrellita(graph, start, end):
    
    return 0

def initGrid(size):
    grid = []               # grid := matriz del mapa entero de tamaño sizexsize.
    for i in range(size):   # Se inicializan los valores de la matriz con 0's.
        row = [0] * size
        grid.append(row)
    return grid

def initRooms(rows):
    grid = initGrid(rows)
    
    rooms = []                          # rooms := rectángulos que representan salas.
    for k in range(25):                
        g = room.generateRoom(rows)     # g := sala de tamaño y coordenadas aleatorias.
        for r in rooms:                 # Checkeo de colisiones con el resto de salas.
            if g.isColliding(r):
                g = None
                break
        if g == None:                   # Si g colisiona no se agrega a grid y se sigue iterando.
            continue
        for i in range(g.x, g.x+g.width):   #  Si g no colisiona se agrega a la grid llenando la zona de 1's.
            for j in range(g.y, g.y+g.length):
                grid[i][j] = 1
        rooms.append(g)                     # se agrega g a la lista de salas válidas.
    return grid, rooms

def generateGraph(rooms):   # Creación del grafo mediante triangulación de Delaunay.
    centers = np.empty([len(rooms),2])
    for i in range(len(rooms)):
        centers[i,0] = rooms[i].centerx
        centers[i,1] = rooms[i].centery
    return centers[Delaunay(centers).simplices]
    
def initGame(rows):
    grid, rooms = initRooms(rows)
    graph = generateGraph(rooms)
    return grid,rooms,graph

def main():
    size = 1000
    rows = 50
    grid,rooms,triangles = initGame(rows)

    window = pygame.display.set_mode((size,size),pygame.RESIZABLE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                size = max([event.h,event.w])
                window = pygame.display.set_mode((size, size),
                                              pygame.RESIZABLE)
        redraw(window,size/rows,grid,rooms,triangles)

main()
