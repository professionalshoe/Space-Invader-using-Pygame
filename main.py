import pygame
import io
#game initialisation
pygame.init()
#creating screen
screen = pygame.display.set_mode((800,600))
running= True
#player
playerimg = pygame.image.load("HEROPLANE1.svg").convert()
playerX = 370
playerY=480
size=(64,64)
playerimg = pygame.transform.scale(playerimg,size)

def player():
        screen.blit(playerimg,(playerX,playerY))
#game loop
while running:
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                        running = False


        player()
        pygame.display.update()