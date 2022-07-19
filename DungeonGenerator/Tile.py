import copy
import random

class Tile:
	
	def __init__(self, corners):
		# corners := elementos pertenecientes a las esquinas de la baldosa
		# [0] := IZQ-SUP, [1] := DER-SUP
		# [3] := IZQ-INF, [2] := DER-INF
		self.COLORS = [(3, 88, 140),(255,255,255),(255, 51, 82)]
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
	def getColors(self):
		COLORS = self.COLORS
		corners = self.corners
		return([ COLORS[corners[0]], COLORS[corners[1]], COLORS[corners[2]], COLORS[corners[3]] ])

def getValues(coors,roomGrid,tiles):
	i = coors[0]
	j = coors[1]
	values = list(range(len(tiles)))
	if i < len(roomGrid)-1 and roomGrid[i+1][j] != -1:
		nright = tiles[roomGrid[i+1][j]].left
		values = [val for val in values if tiles[val] in nright]
	# Consideramos valores posibles que puede tener a la derecha la baldosa a la izquierda
	if i > 0 and roomGrid[i-1][j] != -1:
		nleft = tiles[roomGrid[i-1][j]].right
		values = [val for val in values if tiles[val] in nleft]
	# Consideramos valores posibles que puede tener abajo la baldosa de arriba
	if j > 0 and roomGrid[i][j-1] != -1:
		nup = tiles[roomGrid[i][j-1]].down
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
				minval = getValues((i,j),roomGrid,tiles)
				break
		if minval != None:
			break
	for i,row in enumerate(roomGrid):
		for j,val in enumerate(row):
			if roomGrid[i][j] == -1 and len(getValues((i,j),roomGrid,tiles)) < len(minval):
				minval = getValues((i,j),roomGrid,tiles)
	min_arr = []
	for i,row in enumerate(roomGrid):
		for j,val in enumerate(row):
			if roomGrid[i][j] == -1 and len(getValues((i,j),roomGrid,tiles)) == len(minval):
				min_arr.append([(i,j),getValues((i,j),roomGrid,tiles)])
	if len(min_arr) > 0:
		sel = random.choice(min_arr)
		coors[0] = sel[0][0]
		coors[1] = sel[0][1]
		minval = sel[1]
	return coors, minval

def isComplete(roomGrid):
	for row in roomGrid:
		for val in row:
			if val == -1:
				return False
	return True
def waveFunctionCollapse(roomGrid,tiles,wh,roomc):

	# while not isComplete(roomGrid):
	# 	coors,var = getMostConstrained(roomGrid,tiles)
	# 	#random.shuffle(var)
	# 	if len(var) > 0:
	# 		value = random.choice(var)
	# 		roomGrid[coors[0]][coors[1]] = value
	# 		if value != 0:
	# 			wh.addTile(roomc[0]+coors[0],roomc[1]+coors[1], tiles[value].getColors())
	# 			#wh.addBox(roomc[0]+coors[0],roomc[1]+coors[1],(124, 5, 242))
	# 			wh.update()
	# 	else:
	# 		roomGrid[coors[0]][coors[1]] = 0

	if isComplete(roomGrid):
		return roomGrid
	coors,var = getMostConstrained(roomGrid,tiles)
	random.shuffle(var)
	for value in var:
		roomGrid[coors[0]][coors[1]] = value
		if value != 0:
			wh.addTile(roomc[0]+coors[0],roomc[1]+coors[1], tiles[value].getColors())
			wh.update()
		result = waveFunctionCollapse(roomGrid,tiles,wh,roomc)
		if result != None:
			return result
		roomGrid[coors[0]][coors[1]] = -1
		if value != 0:
			wh.addBox(roomc[0]+coors[0],roomc[1]+coors[1],(3, 88, 140))
			wh.update()
	return None




