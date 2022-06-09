import stage_creation
import pygame

pygame.init()

win = pygame.display.set_mode(1000, 1000)

pygame.display.set_caption("Untitled rogue game")

x = 50
y = 50
width = 40
height = 60
vel = 5

run = true
while run:
    pygame.display.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.draw.rect(win, (255, 0 , 0), (x, y, width))
    
pygame.quit()