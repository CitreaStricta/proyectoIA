import copy
import random

class Tile:
	def __init__(self, corners):
		# corners := elementos pertenecientes a las esquinas de la baldosa
		# [0] := IZQ-SUP, [1] := DER-SUP
		# [3] := IZQ-INF, [2] := DER-INF
		self.corners = corners
		self.up = []
		self.down = []
		self.left = []
		self.right = []
	def setNeighbors(self,neighbors):
		for n in neighbors:
			if self.validneighbor(n,0):
				self.up.append(n)
			if self.validneighbor(n,1):
				self.right.append(n)
			if self.validneighbor(n,2):
				self.down.append(n)
			if self.validneighbor(n,3):
				self.left.append(n)
	def validneighbor(self,t,pos):
		# pos := ṕosición relativa de t a self
		socket1 = t.corners[(3+pos)%4]
		socket2 = t.corners[(2+pos)%4]
		return (socket1==self.corners[0+pos] and socket2==self.corners[(1+pos)%4])


def getValues(coors,roomGrid,tiles):
	i = coors[0]
	j = coors[1]
	values = list(range(len(tiles)))
	if i < len(roomGrid)-1 and roomGrid[i+1][j] != -1:
		nright = tiles[roomGrid[i-1][j]].left
		values = [val for val in values if tiles[val] in nright]
	# Consideramos valores posibles que puede tener a la derecha la baldosa a la izquierda
	if i > 0 and roomGrid[i-1][j] != -1:
		nleft = tiles[roomGrid[i-1][j]].right
		values = [val for val in values if tiles[val] in nleft]
	# Consideramos valores posibles que puede tener abajo la baldosa de arriba
	if j > 0 and roomGrid[i][j-1] != -1:
		nup = tiles[roomGrid[i-1][j]].down
		values = [val for val in values if tiles[val] in nup]
	# Consideramos valores posibles que puede tener arriba la baldosa de abajo
	if j < len(roomGrid[i])-1 and roomGrid[i][j+1] != -1:
		ndown = tiles[roomGrid[i][j+1]].up
		values = [val for val in values if tiles[val] in ndown]
	return values

def getMostConstrained(roomGrid,tiles):
	minval = None
	coors = [-1,-1]
	for i,row in enumerate(roomGrid):
		for j,val in enumerate(row):
			if val == -1:
				coors[0] = i
				coors[1] = j
				minval = getValues(coors,roomGrid,tiles)
				break
		if minval != None:
			break
	for i,row in enumerate(roomGrid):
		for j,val in enumerate(row):
			if roomGrid[i][j] == -1 and len(getValues((i,j),roomGrid,tiles)) < len(minval):
				minval = getValues((i,j),roomGrid,tiles)
				coors[0] = i
				coors[1] = j
	return coors, minval

def isComplete(roomGrid):
	for row in roomGrid:
		for val in row:
			if val == -1:
				return False
	return True
def recursiveBacktracking(roomGrid,tiles,wh,roomc,iteration=-1):
	if isComplete(roomGrid):
		return roomGrid
	iteration_a = iteration + 1
	print(f'iteration: {iteration}')
	coors,var = getMostConstrained(roomGrid,tiles)
	random.shuffle(var)
	for value in var:
		roomGrid[coors[0]][coors[1]] = value
		if value != 0:
			wh.addBox(roomc[0]+coors[0],roomc[1]+coors[1],(124, 5, 242))
			wh.update()
		result = recursiveBacktracking(roomGrid,tiles,wh,roomc,iteration_a)
		if result != None:
			return result
		roomGrid[coors[0]][coors[1]] = -1
		if value != 0:
			wh.addBox(roomc[0]+coors[0],roomc[1]+coors[1],(3, 88, 140))
			wh.update()
	return None


def waveFunctionCollapse(roomGrid,tiles):
	# roomgrid[i][j]=-1 := no hay nada aquí
	# roomgrid[i][j]=0 := hay tile[0] en i,j
	# posibleValues = []	# := matriz de valores posibles
	# for i,row in enumerate(roomGrid):
	# 	valuerow = []
	# 	for j,val in enumerate(row):
	# 		if val != 0:
	# 			values = tiles.view()	# al inicio consideramos todas las baldosas posibles para i,j
	# 			values = getValues((i,j),roomGrid,tiles,values)
	# 			# vamos removiendo valores posibles según restricciónes
	# 		else:
	# 			values = []
	# 		valuerow.append(values)
	# 	posibleValues.append(valuerow)
	return recursiveBacktracking(roomGrid,tiles)


	# TODO -----------------------
	# - Encontrar coordenadas de espacio con menor canitdad de baldosas posibles
	# (de entre todas las casillas con valor -1)(si hay empate se toma solo 1, 
	#  da lo mismo sistema de elección)
	# - Definir un valor para casilla con menor valor
	# - Terminar algoritmo cuando no se encuentren casillas con valor -1
	# - Hay que implementar backtracking pues pueden haber casos en los que no haya niguna solución posible
