from DungeonGenerator.A_star import a_star
from scipy.spatial import Delaunay
from scipy.sparse.csgraph import minimum_spanning_tree
import pygame
import numpy as np
from DungeonGenerator.Room import room
#from window_handler import windowHandler
from DungeonGenerator.Window import Window
import room_content
import random

class Generator:
	def __init__(self,size=700):
		self.size = size
		self.rooms = []
		self.graph = []
		self.paths = []
	def initGrid(self,nrows):
	    grid = []               # grid := matriz del mapa entero de tamaño sizexsize.
	    for i in range(nrows):   # Se inicializan los valores de la matriz con 0's.
	        row = [0] * nrows
	        grid.append(row)
	    return grid
	def generateRooms(self):
		grid = self.grid   # Se crea una matriz de 0's rowsxrows
		rows = self.rows
		wh = self.wh
		rooms = []                          # rooms := rectángulos que representan salas.
		for k in range(50):
			g = room.generateRoom(rows)     # g := sala de tamaño y coordenadas aleatorias.
			if g.isCollidingMany(rooms):
				continue
			for i in range(g.x, g.x+g.width):   #  Si g no colisiona se agrega a la grid llenando la zona de 1's.
				for j in range(g.y, g.y+g.length):
					wh.addBox(i,j,(3, 88, 140),1)
					grid[i][j] = 1
					#wh.redraw(grid,rooms)
					wh.update()
			wh.addPoint(g.centerx,g.centery,(105, 158, 191))
			rooms.append(g)                     # se agrega g a la lista de salas válidas.
		self.rooms = rooms
		self.grid = grid

	def generateGraph(self):   # Creación del grafo mediante triangulación de Delaunay.
		rooms = self.rooms
		wh = self.wh
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

		for i in range(len(mst)):
			for j in range(len(mst)):
				if mst[i][j] != 0:
					wh.addLine((centers[i][0], centers[i][1]),(centers[j][0], centers[j][1]), (3, 140, 127))
					wh.update()
		self.graph = mst
	def getPaths(self):
		graph = self.graph
		grid = self.grid
		rooms = self.rooms
		wh = self.wh
		for i in range(len(graph)):
		    for j in range(len(graph)):
		        if graph[i][j] != 0:
		            grid = a_star(grid,rooms[i],rooms[j],wh)
		            #self.paths.append(path)

		self.grid = grid
	def roomPath(self):
		grid = self.grid
		rooms = self.rooms
		wh = self.wh

		entradas = []
		size = len(grid)
		idx = -1

		print(size)

		for r in rooms:
		    entradas.append([])
		    idx = idx + 1
		    for i in range(r.x, r.x + r.width):
		        for j in range(r.y, r.y + r.length):
		            if i-1 >= 0:
		                if grid[i-1][j] == 4:
		                    grid[i][j] = 5
		                    entradas[idx].append([i,j])
		                    wh.addBox(i,j,(255, 102, 178))
		            if i+1 < size:
		                if grid[i+1][j] == 4:
		                    grid[i][j] = 5
		                    entradas[idx].append([i,j])
		                    wh.addBox(i,j,(255, 102, 178))
		            if j+1 < size:
		                if grid[i][j+1] == 4:
		                    grid[i][j] = 5
		                    entradas[idx].append([i,j])
		                    wh.addBox(i,j,(255, 102, 178))
		            if j-1 >= 0:
		                if grid[i][j-1] == 4:
		                    grid[i][j] = 5
		                    entradas[idx].append([i,j])
		                    wh.addBox(i,j,(255, 102, 178))

		return entradas
	def init_content(self):
		rooms = self.rooms
		grid = self.grid
		wh = self.wh
		contenidos = []
		for room in rooms:
			# se crean casillas que "pegan"
			contenido = room_content.trampa(room, random.randint(0, room.width-1), random.randint(0, room.length-1))
			grid[contenido.content_x_pos][contenido.content_y_pos] = 6
			wh.addBox(contenido.content_x_pos,contenido.content_y_pos,(255,127,80))
			# se crean casillas donde el jugador no se puede colocar
			contenido = room_content.roca(room, random.randint(0, room.width-1), random.randint(0, room.length-1))
			grid[contenido.content_x_pos][contenido.content_y_pos] = 7
			wh.addBox(contenido.content_x_pos,contenido.content_y_pos,(6, 32, 39))
			# FALTA HACER EL CHEKEO DE QUE NO SE PONGAN UNA ENCIMA DE LA OTRA


			contenidos.append(contenido)

		return contenidos
	def generateDungeon(self,rows=50):
		size = self.size
		self.rows = rows
		wh = Window(size,rows)
		grid = self.initGrid(rows)
		self.grid = grid
		self.wh = wh
		self.generateRooms()
		self.generateGraph()
		self.getPaths()
		self.roomPath()
		contenidos = self.init_content()
		while True:
			wh.update()
			if wh.reset:
				wh.clear()
				break