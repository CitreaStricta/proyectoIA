import pygame
class windowHandler:
    def __init__(self, window,blockSize):
        self.window = window
        self.blockSize = blockSize
        self.graph = []
        self.rooms = []
        self.reset = False
    def drawGrid(self, grid):  # Dibujo de mapas (Salas, túneles, fondo, etc.).
        bs = self.blockSize
        win = self.window
        for i in range(len(grid)):
            for j in range(len(grid)):
                rect = pygame.Rect(i*bs+0.5, j*bs+0.5, bs-1, bs-1)
                if grid[i][j] == 1:
                    pygame.draw.rect(win, (3, 88, 140), rect)
                elif grid[i][j] == 2:
                    pygame.draw.rect(win, (105, 158, 191), rect)
                elif grid[i][j] == 3:
                    pygame.draw.rect(win, (242, 234, 114), rect)
                elif grid[i][j] == 4:
                    pygame.draw.rect(win, (56, 134, 154), rect)
                elif grid[i][j] == 5:
                    pygame.draw.rect(win, (255, 102, 178), rect)
                else:
                    pygame.draw.rect(win, (1, 13, 38), rect)

    def drawCenters(self, rooms):  # Dibujo de puntos centrales de cada sala.
        bs = self.blockSize
        win = self.window
        for r in rooms:
            pygame.draw.circle(win, (105, 158, 191), (r.centerx*bs, r.centery*bs), 5)

    def handleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.image.save( window, 'surface.png' )
                exit()
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                size = event.w
                self.window = pygame.display.set_mode((size, size),
                                              pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset = True

    def drawGraph(self, graph, rooms):    # Dibujo de líneas de grafo
        bs = self.blockSize
        win = self.window
        for i in range(len(graph)):
            for j in range(len(graph)):
                if graph[i][j] != 0:
                    p1 = (rooms[i].centerx*bs, rooms[i].centery*bs)
                    p2 = (rooms[j].centerx*bs, rooms[j].centery*bs)
                    pygame.draw.line(win, (3, 140, 127), p1, p2)
    def setGraph(self, rooms, graph):
        self.rooms = rooms
        self.graph = graph

    def redraw(self, grid, rooms=[]):
        self.window.fill((0, 3, 13))
        self.drawGrid(grid)
        if len(rooms) != 0:
            self.drawCenters(rooms)
        elif len(self.graph) != 0:
            self.drawCenters(self.rooms)
            self.drawGraph(self.graph,self.rooms)
        
        pygame.display.update()