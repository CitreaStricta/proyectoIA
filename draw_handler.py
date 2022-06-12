import pygame

def drawGrid(window, blockSize, grid):  # Dibujo de mapas (Salas, túneles, fondo, etc.).
    for i in range(len(grid)):
        for j in range(len(grid)):
            rect = pygame.Rect(i*blockSize+0.5, j*blockSize+0.5, blockSize-1, blockSize-1)
            if grid[i][j] == 1:
                pygame.draw.rect(window, (3, 88, 140), rect)
            elif grid[i][j] == 2:
                pygame.draw.rect(window, (105, 158, 191), rect)
            else:
                pygame.draw.rect(window, (1, 13, 38), rect)

def drawCenters(window, blockSize, rooms):  # Dibujo de puntos centrales de cada sala.
    for r in rooms:
        pygame.draw.circle(window, (105, 158, 191), (r.centerx*blockSize, r.centery*blockSize), 5)

def drawGraph(window, blockSize, graph,rooms):    # Dibujo de líneas de grafo
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] != 0:
                p1 = (rooms[i].centerx*blockSize, rooms[i].centery*blockSize)
                p2 = (rooms[j].centerx*blockSize, rooms[j].centery*blockSize)
                pygame.draw.line(window, (3, 140, 127), p1, p2)

    #for t in triangles:
    #    p = t*blockSize
    #    pygame.draw.polygon(window, (3, 140, 127), points=p, width=2)

def redraw(window, blockSize, grid, rooms, graph):
    window.fill((0, 3, 13))
    
    drawGrid(window, blockSize, grid)
    drawCenters(window, blockSize, rooms)
    drawGraph(window, blockSize, graph,rooms)
    
    pygame.display.update()