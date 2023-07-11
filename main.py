"""
Oi! Este é o arquivo pincipal da nossa implementação do MENACE - desenvolvido utilizando
a biblioteca pygame.

:)
"""

# Importações
import pygame, sys
from files.gui import *
from files.api import *


# ------------------------------------ Configurações iniciais
pygame.init()
clock = pygame.time.Clock()
running = True
FPS = 60
pausado = [False, False]
pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.MOUSEBUTTONDOWN])
font = pygame.font.Font('files/assets/basis33.ttf', 50)
loading = True

lista_konami = ['0' for _ in range(10)]

# Janela:
screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H),pygame.FULLSCREEN|pygame.SCALED)
pygame.display.set_caption('MENACE')
icon = pygame.image.load('files/assets/icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('files/assets/sprites/bg_colorido.png')
background = pygame.transform.scale_by(background, scale_factor)
pygame.mouse.set_visible(False)

# Placar:
vitorias_jogador = [0]
vitorias_menace = [0]
empates = [0]
lista_de_listas = [vitorias_jogador, vitorias_menace, empates]


# ------------------------------------ Instâncias e objetos 
# Jogador:
Player_group = pygame.sprite.Group()

player = Player(isX_constant, (100, 100))
Player_group.add(player)

# Menace:
menace = Menace(not player.isX)
if loading: menace.load_pickles(lista_de_listas)

# Animação:
animacao_group = pygame.sprite.Group()
proximo_group = pygame.sprite.GroupSingle()

proximo = pygame.sprite.Sprite()
proximo.image = pygame.image.load('files/assets/sprites/spr_proximo.png').convert_alpha()
proximo.image = pygame.transform.scale_by(proximo.image, scale_factor)
proximo.rect = proximo.image.get_rect()
proximo.rect.center = display_center
proximo_group.add(proximo)

# Caixinhas:
caixinhas_group = pygame.sprite.Group()

for i in range(9):
    caixinha_nova = Caixinhas(player,i+1)
    caixinhas_group.add(caixinha_nova)
    
# Probabilidades:
prob_group = pygame.sprite.Group()

for i in range(9):
    prob_nova = Probabilidades('0%',i+1,screen,font)
    prob_group.add(prob_nova)


# ------------------------------------ Loop do jogo
while running:
    events = pygame.event.get()
    
    lista_konami = konami(events, lista_konami)
    if lista_konami == True:
        menace.save_pickles(lista_de_listas)
        running = False

    # Checagem de eventos:
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                print(menace.menace.brain)
            if event.key == pygame.K_h:
                print(f"------------------------ \
\n Vitórias do jogador: {lista_de_listas[0][-1]} \n \
\n Vitórias do MENACE: {lista_de_listas[1][-1]} \n \
\n Empates: {lista_de_listas[2][-1]} \n \
------------------------")
            if event.key == pygame.K_r and not pausado[0]:
                animacao_group.empty()
                pausado[0] = True
                reset_game(caixinhas_group)
                menace.menace.jogadas = []
                mixer.stop()
            if pausado and event.key == pygame.K_RETURN:
                animacao_group.empty()
                pausado[0] = False
                if pausado[1]:
                    pausado[0] = True
                    pausado[1] = False
                    reset_game(caixinhas_group)
                mixer.stop()
    
    if pausado[1]:
        pausado[1] -= 1
        if not pausado[1]:
            reset_game(caixinhas_group)
    
    if (player.isX) and (get_string(caixinhas_group) == '000000000') and (not pausado[0]):
        menace.jogada(caixinhas_group, lista_de_listas, animacao_group, pausado, prob_group)

    # Updates:
    if (not pausado[0]) or (pausado[1]):
        screen.blit(background,(0, 0))
        
        caixinhas_group.draw(screen)
        caixinhas_group.update(events, menace, caixinhas_group, lista_de_listas, animacao_group, pausado, prob_group)
    
    if ((len(animacao_group) != 0) or (pausado[0])) and (not pausado[1]): screen.fill((0,0,0))
    if ((len(animacao_group) == 0) and (pausado[0])) and (not pausado[1]): proximo_group.draw(screen)
    
    if (not pausado[0]) or (pausado[1]):
        prob_group.draw(screen)
        prob_group.update()
        
        if (len(animacao_group) == 0):
            Player_group.draw(screen)
            Player_group.update()
            
    animacao_group.draw(screen)
    animacao_group.update()
    
    pygame.display.update()
    clock.tick(FPS)

# Fecha loop do jogo:    
pygame.quit()
sys.exit()
