import pygame
class Window:
	def __init__(self,size,rows):
		self.boxes = []
		for i in range(rows):   # Se inicializan los valores de la matriz con 0's.
			row = [((1, 13, 38),0)] * rows
			self.boxes.append(row)
		self.lines = []
		self.points = []
		self.tiles = []
		self.rows = rows
		self.size = size
		self.window = pygame.display.set_mode((size,size),pygame.RESIZABLE)
		self.reset = False
	def addTile(self,x,y,colors):
		self.tiles.append(((x,y),colors))
	def addBox(self,x,y,color,boxid=0):
		self.boxes[x][y] = (color,boxid)
	def addLine(self,p1,p2,color,lineid=0):
		self.lines.append(	((p1,p2),color,lineid)	)
	def addPoint(self,x,y,color,pointid=0):
		self.points.append(	((x,y),color,pointid)	)
	def drawTiles(self):
		bs = self.size/self.rows
		win = self.window
		rows = self.rows
		tiles = self.tiles
		for t in tiles:
			x = t[0][0]
			y = t[0][1]
			side = (bs-1)/2
			rect = []
			rect.append(pygame.Rect(x*bs+0.5, y*bs+0.5, side, side))
			rect.append(pygame.Rect(x*bs+0.5+side, y*bs+0.5, side, side))
			rect.append(pygame.Rect(x*bs+0.5+side, y*bs+0.5+side, side, side))
			rect.append(pygame.Rect(x*bs+0.5, y*bs+0.5+side, side, side))
			for i, r in enumerate(rect):
				pygame.draw.rect(win, t[1][i], r)
	def drawBoxes(self):
		bs = self.size/self.rows
		win = self.window
		rows = self.rows
		boxes = self.boxes
		for x in range(rows):
			for y in range(rows):
				color = boxes[x][y][0]
				rect = pygame.Rect(x*bs+0.5, y*bs+0.5, bs-1, bs-1)
				pygame.draw.rect(win, color, rect)
	def drawPoints(self):
		bs = self.size/self.rows
		win = self.window
		points = self.points
		for point in points:
			x = point[0][0]
			y = point[0][1]
			color = point[1]
			pygame.draw.circle(win, color, (x*bs, y*bs), 5)
	def drawLines(self):
		bs = self.size/self.rows
		win = self.window
		lines = self.lines
		for line in lines:
			p1 = line[0][0]
			p2 = line[0][1]
			color = line[1]
			p1 = (p1[0]*bs,p1[1]*bs)
			p2 = (p2[0]*bs,p2[1]*bs)
			pygame.draw.line(win, color, p1, p2)
	def deleteBoxes(self, boxId):
		boxes = self.boxes
		rows = self.rows
		for i in range(rows):
			for j in range(rows):
				if boxes[i][j][1] == boxId:
					boxes[i][j] = ((1, 13, 38),0)
		self.boxes = boxes
	def handleEvent(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.VIDEORESIZE:
				size = event.w
				self.size = size
				self.window = pygame.display.set_mode((size, size),
											  pygame.RESIZABLE)
			if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
				self.reset = True
	def clear(self):
		self.boxes = []
		self.lines = []
		self.points = []
	def update(self):
		self.handleEvent()
		self.window.fill((0, 3, 13))
		self.drawBoxes()
		self.drawLines()
		self.drawPoints()
		self.drawTiles()
		pygame.display.update()