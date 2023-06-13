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

player = Player(True, (100, 100))
Player_group.add(player)

# Menace:
menace = Menace(not player.isX)

# Animação:
animacao_group = pygame.sprite.Group()

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
            menace.save_pickle()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print(menace.menace.brain)
    
    if player.isX and get_string(caixinhas_group) == '000000000':
        menace.jogada(caixinhas_group, lista_de_listas, animacao_group)

    # Updates:
    screen.blit(background,(0, 0))
    
    caixinhas_group.draw(screen)
    caixinhas_group.update(events, menace, caixinhas_group, lista_de_listas, animacao_group)
    
    Player_group.draw(screen)
    Player_group.update()
    
    if len(animacao_group) != 0: screen.fill((0,0,0))
    
    animacao_group.draw(screen)
    animacao_group.update()
    
    pygame.display.update()
    clock.tick(FPS)

    
pygame.quit()
sys.exit()