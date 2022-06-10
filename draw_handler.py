import pygame

def drawGrid(window, blockSize, grid):  # Dibujo de mapas (Salas, túneles, fondo, etc.).
    for i in range(len(grid)):
        for j in range(len(grid)):
            rect = pygame.Rect(i*blockSize+0.5, j*blockSize+0.5, blockSize-1, blockSize-1)
            if grid[i][j] == 1:
                pygame.draw.rect(window, (3, 88, 140), rect)
            else:
                pygame.draw.rect(window, (1, 13, 38), rect)

def drawCenters(window, blockSize, rooms):  # Dibujo de puntos centrales de cada sala.
    for r in rooms:
        pygame.draw.circle(window, (105, 158, 191), (r.centerx*blockSize, r.centery*blockSize), 5)

def drawGraph(window, blockSize, triangles):    # Dibujo de líneas de grafo
    for t in triangles:
        p = t*blockSize
        pygame.draw.polygon(window, (3, 140, 127), points=p, width=2)

def redraw(window, blockSize, grid, rooms, triangles):
    window.fill((0, 3, 13))
    
    drawGrid(window, blockSize, grid)
    drawCenters(window, blockSize, rooms)
    drawGraph(window, blockSize, triangles)
    
    pygame.display.update()