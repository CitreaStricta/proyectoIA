import pygame
from scipy.spatial import Delaunay
from scipy.sparse.csgraph import minimum_spanning_tree
import numpy as np
from stage_models import room
from draw_handler import redraw
import random

def a_estrellita(graph, start, end):
    
    return 0

def initGrid(size):
    grid = []               # grid := matriz del mapa entero de tamaño sizexsize.
    for i in range(size):   # Se inicializan los valores de la matriz con 0's.
        row = [0] * size
        grid.append(row)
    return grid

def initRooms(rows):
    grid = initGrid(rows)   # Se crea una matriz de 0's rowsxrows

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
    # Crear una matriz vacía len(rooms)xlen(rooms) -> M
    m = np.zeros((len(rooms),len(rooms)))
    # Iterando en los simplices t -> simplex
    #   t[0]-t[1] -> verificar si arista existe
    #   Hacer lo mismo para t[1]-t[2]
    #   hacer lo mismo para t[0]-t[2]
    #   si no existe t[a]-t[b] en M insertar en M[min(t[a],t[b]),max(t[a],t[b])]: distancia entre centers[t[a]] y centers[t[b]]
    #   Si arista existe, seguir iterando
    for t in Delaunay(centers).simplices:
        if m[t[0]][t[1]] == 0:
            if t[0] < t[1]:
                m[t[0]][t[1]] = np.linalg.norm(t[1] - t[0])
            else:
                m[t[1]][t[0]] = np.linalg.norm(t[0] - t[1])
        if m[t[1]][t[2]] == 0:
            if t[1] < t[2]:
                m[t[1]][t[2]] = np.linalg.norm(t[2] - t[1])
            else:
                m[t[2]][t[1]] = np.linalg.norm(t[1]- t[2])
        if m[t[0]][t[2]] == 0:
            if t[0] < t[2]:
                m[t[0]][t[2]] = np.linalg.norm(t[2] - t[0])
            else:
                m[t[2]][t[0]] = np.linalg.norm(t[0] - t[2])        

    # Calcular mst (llamar función scipy)
    mst = minimum_spanning_tree(m).toarray().astype(int)



    # Restar mst a M para obtener aristas no agregadas
    no_agregadas = m - mst
    
    # Agregar aristas aleatoriamente desde M a mst con una probabilidad elegida.
    for i in range(len(no_agregadas)):
        for j in range(len(no_agregadas)):
            if no_agregadas[i][j] != 0:
                if random.randint(0,5) == 1:
                    mst[i][j] = no_agregadas[i][j]

    return mst
    
def initGame(rows):
    grid, rooms = initRooms(rows)   # Se inicializa la grilla y la lista de salas
    graph = generateGraph(rooms)
    return grid,rooms,graph

def main():
    size = 700     # Tamaño de la pantalla
    rows = 50       # rows := cantidad de filas y columnas de la grilla

    grid,rooms,graph = initGame(rows)

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
        redraw(window,size/rows,grid,rooms,graph)

main()
