import pygame
from scipy.spatial import Delaunay
from scipy.sparse.csgraph import minimum_spanning_tree
import numpy as np
from stage_models import room
from draw_handler import redraw
import random

def getDistToRoom(x,y,room):
    if room.x <= x <= room.x + room.width:
        return min(abs(room.y - y),abs(y - (room.y+room.length)))
    if room.y <= y <= room.y + room.length:
        return min(abs(room.x - x),abs(x - (room.x+room.width)))
    if x <= room.x:
        return min( np.linalg.norm([x-room.x, y-room.y]),
                    np.linalg.norm([x-room.x, (y-(room.y+ room.length))]))
    if x >= room.x+room.width:
        return min( np.linalg.norm([x-(room.x+room.width), y-room.y]),
                    np.linalg.norm([x-(room.x+room.width), y-(room.y+ room.length)]))
class APriorityQueue(object):
    def __init__(self):
        self.queue = []
 
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
    def __len__(self):
        return len(self.queue)

    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self, data):
        self.queue.append(data)

    def pop(self):
        try:
            min_val = 0
            for i in range(len(self.queue)):
                if self.queue[i][1] < self.queue[min_val][1]:
                    min_val = i
            item = self.queue[min_val]
            del self.queue[min_val]
            return item
        except IndexError:
            print()
            exit()
def initFrontier(grid, r_start):
    front = []
    if r_start.x > 0:
        for i in range(r_start.length):
            front.append((r_start.x-1,r_start.y+i))
    if r_start.x + r_start.width < len(grid)-1:
        for i in range(r_start.length):
            front.append((r_start.x+r_start.width,r_start.y+i))
    if r_start.y > 0:
        for i in range(r_start.width):
            front.append((r_start.x+i,r_start.y-1))
    if r_start.y + r_start.length < len(grid)-1:
        for i in range(r_start.width):
            front.append((r_start.x+i,r_start.y+r_start.length))
    return front

def a_star(grid, r_start, r_end):
    #root = [getClosestStart(grid, r_start, r_end),0]#[(int(r_start.centerx),int(r_start.centery)),0]    #tupla con f
    frontier = APriorityQueue()
    #frontier.insert(root)
    #print(str(r_start.x) + "," +  str(r_start.y) + "-" + str(r_end.x) + "," + str(r_end.y))
    camino = {}
    g = {}
    #camino[root[0]] = None
    #g[root[0]] = 0
    for i in initFrontier(grid, r_start):
        cost = 1
        g[i] = cost
        h = getDistToRoom(i[0],i[1],r_end)
        f = cost + h
        frontier.insert([i,f])
        camino[i] = None

    last: Tuple[int,int]
    while not frontier.isEmpty():
        current = frontier.pop()
        if getDistToRoom(current[0][0]+0.5,current[0][1]+0.5,r_end) == 0.5:
            last = current[0]
            break
        neighbors = []
        if current[0][0] > 0 and grid[current[0][0]-1][current[0][1]] != 1:
            neighbors.append((current[0][0]-1,current[0][1]))
        if current[0][1] > 0 and grid[current[0][0]][current[0][1]-1] != 1:
            neighbors.append((current[0][0],current[0][1]-1))
        if current[0][0] < len(grid)-1 and grid[current[0][0]+1][current[0][1]] != 1:
            neighbors.append((current[0][0]+1,current[0][1]))
        if current[0][1] < len(grid)-1 and grid[current[0][0]][current[0][1]+1] != 1:
            neighbors.append((current[0][0],current[0][1]+1))
        for n in neighbors:
            cost = g[current[0]] + 1
            if n not in g or cost < g[n]:
                g[n] = cost
                h = getDistToRoom(n[0],n[1],r_end)
                f = cost + h
                frontier.insert([n,f])
                camino[n] = current[0]
        
    print(last[0])
    while camino[last] != None:
        if grid[last[0]][last[1]] != 1:
            grid[last[0]][last[1]] = 2
        last = camino[last]
    if grid[last[0]][last[1]] != 1:
            grid[last[0]][last[1]] = 2
    return grid

def getPaths(graph,grid,rooms):
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] != 0:
                grid = a_star(grid,rooms[i],rooms[j])
    return grid

def initGrid(size):
    grid = []               # grid := matriz del mapa entero de tamaño sizexsize.
    for i in range(size):   # Se inicializan los valores de la matriz con 0's.
        row = [0] * size
        grid.append(row)
    return grid

def initRooms(rows):
    grid = initGrid(rows)   # Se crea una matriz de 0's rowsxrows

    rooms = []                          # rooms := rectángulos que representan salas.
    for k in range(50):
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
    grid = getPaths(graph,grid,rooms)
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
