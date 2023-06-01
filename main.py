"""
Oi! Este é o arquivo pincipal da nossa implementação do MENACE - desenvolvido utilizando
a biblioteca pygame.

:)
"""


import pygame, sys
from files.gui import *
from files.api import *


# ------------------------------------ Configurações iniciais
pygame.init()
clock = pygame.time.Clock()
running = True
FPS = 60

# Janela:
DISPLAY_W, DISPLAY_H = 1280, 960
screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
pygame.display.set_caption('MENACE')
icon = pygame.image.load('files/assets/icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('files/assets/sprites/bg.png')
background = pygame.transform.scale_by(background, scale_factor)
pygame.mouse.set_visible(False)

# Placar:
vitorias_jogador = [0]
vitorias_menace = [0]
empates = [0]
lista_de_listas = [vitorias_jogador, vitorias_menace, empates]


# ------------------------------------ Instâncias e objetos 
# Player:
Player_group = pygame.sprite.Group()

player = Player(False, (100, 100))
Player_group.add(player)

# Menace:
menace = Menace(not player.isX)

# Caixinhas:
caixinhas_group = pygame.sprite.Group()

for i in range(9):
    caixinha_nova = Caixinhas(player,i+1)
    caixinhas_group.add(caixinha_nova)


# ------------------------------------ Loop do jogo
while running:
    events = pygame.event.get()
    
    # Close event check:
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Updates:
    screen.blit(background,(0, 0))
    
    caixinhas_group.draw(screen)
    caixinhas_group.update(events, menace, caixinhas_group, lista_de_listas)
    
    Player_group.draw(screen)
    Player_group.update()
    
    pygame.display.flip()
    clock.tick(FPS)

    
pygame.quit()
sys.exit()