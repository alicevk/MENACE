"""
Oi! Este é o arquivo pincipal da interface gráfica utilizado na nossa implementação
do MENACE - desenvolvido utilizando a biblioteca pygame.

:)
"""

# (460, 530)

import pygame, sys
from classfuncs import *


# ------------------------------------ Configurações iniciais
pygame.init()
clock = pygame.time.Clock()
running = True
FPS = 60

# Janela:
DISPLAY_W, DISPLAY_H = 1280, 960
screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption('MENACE')
icon = pygame.image.load('files/icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('files/sprites/bg.png')
background = pygame.transform.scale_by(background, scale_factor)
pygame.mouse.set_visible(False)


# ------------------------------------ Sprites e Animações
# Caixinhas:
caixinhas_group = pygame.sprite.Group()

caixinha_central = Caixinhas(lambda x: print('oi'))
caixinhas_group.add(caixinha_central)

# OsAndXs:
OsAndXs_group = pygame.sprite.Group()

X_1 = OsAndXs(100, 100, False)
OsAndXs_group.add(X_1)


# ------------------------------------ Loop do jogo
while running:
    
    # Close event check:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False            

    # Events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    
    # Updates:
    screen.blit(background,(0, 0))
    
    caixinhas_group.draw(screen)
    caixinhas_group.update()
    
    OsAndXs_group.draw(screen)
    OsAndXs_group.update()
    
    pygame.display.flip()
    clock.tick(FPS)

    
pygame.quit()
sys.exit()