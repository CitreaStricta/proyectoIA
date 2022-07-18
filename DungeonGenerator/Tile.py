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
	def validneighbor(t,pos):
		# pos := ṕosición relativa de t a self
		socket1 = t.corners[(3+pos)%4]
		socket2 = t.corners[(2+pos)%4]
		return (socket1==self.corners[0+pos] and socket2==self.corners[(1+pos)%4])
def waveFunctionCollapse(roomGrid,tiles):
	# roomgrid[i][j]=-1 := no hay nada aquí
	# roomgrid[i][j]=0 := hay tile[0] en i,j
	posibleValues = []	# := matriz de valores posibles
	for i,row in enumerate(roomGrid):
		valuerow = []
		for j,val in enumerate(row):
			values = tiles.view()	# al inicio consideramos todas las baldosas posibles para i,j
			# vamos removiendo valores posibles según restricciónes
			# Consideramos valores posibles que puede tener a la izquierda la baldosa a la derecha
			if i < len(roomGrid) and roomGrid[i+1][j] != -1:
				nright = tiles[roomGrid[i-1][j]].left
				values = [val for val in values if val in nright]
			# Consideramos valores posibles que puede tener a la derecha la baldosa a la izquierda
			if i > 0 and roomGrid[i-1][j] != -1:
				nleft = tiles[roomGrid[i-1][j]].right
				values = [val for val in values if val in nleft]
			# Consideramos valores posibles que puede tener abajo la baldosa de arriba
			if j > 0 and roomGrid[i][j-1] != -1:
				nup = tiles[roomGrid[i-1][j]].down
				values = [val for val in values if val in nup]
			# Consideramos valores posibles que puede tener arriba la baldosa de abajo
			if j < len(row) and roomGrid[i][j+1] != -1:
				ndown = tiles[roomGrid[i][j+1]].up
				values = [val for val in values if val in ndown]
			valuerow.append(values)
		posibleValues.append(valuerow)
	# TODO -----------------------
	# - Encontrar coordenadas de espacio con menor canitdad de baldosas posibles
	# (de entre todas las casillas con valor -1)(si hay empate se toma solo 1, 
	#  da lo mismo sistema de elección)
	# - Definir un valor para casilla con menor valor
	# - Terminar algoritmo cuando no se encuentren casillas con valor -1
	# - Hay que implementar backtracking pues pueden haber casos en los que no haya niguna solución posible
