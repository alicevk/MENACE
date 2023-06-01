"""
Este é o arquivo responsável por guardar todas as classes e funções utilizadas na
implementação da interface gráfica do MENACE!

:)
"""

import pygame
from files.api import *
scale_factor = 10 # so every sprite has the same scale

# ------------------------------------ Functions
def get_sprites(size, file):
    '''
    transforms a spritesheet image file into a list of individual pygame sprites.

    Args:
        size (tup): (width, height)_of each individual sprite
        file (str): path to spritesheet image

    Returns:
        sprites (list): list of pygame surfaces/sprites
    '''
    w, h = size
    x, y = (0, 0)
    sheet = pygame.image.load(file).convert_alpha()
    sheet_rect = sheet.get_rect()
    sprites = []
    for _ in range(0, sheet_rect.width - w + 1, w):
        sheet.set_clip(pygame.Rect(x, y, w, h))
        sprite = sheet.subsurface(sheet.get_clip())
        sprite = pygame.transform.scale_by(sprite, scale_factor)
        sprites.append(sprite)
        x += w
    return sprites


def get_string(grupo_caixas):
    saida = ''
    for caixa in grupo_caixas:
        saida += str(int(caixa.value))
    return saida


def atualizar_tela(grupo_caixas, jogada_antiga, jogada_atual):
    for caixa, valor_antigo, valor_atual in zip(grupo_caixas, jogada_antiga, jogada_atual.lista):
        if valor_antigo != str(valor_atual): caixa.change_value(valor_atual)
        
        
def vitoria(quem_ganhou, lista_de_listas, menace=None):
    lista_jogador, lista_menace, lista_empates = lista_de_listas
    if quem_ganhou=='p':
        menace.atualizar_derrota()
        lista_jogador.append(lista_jogador[-1]+1)
        lista_menace.append(lista_menace[-1])
        print('Você ganhou!')
    else:
        quem_ganhou.atualizar_vitoria()
        lista_jogador.append(lista_jogador[-1])
        lista_menace.append(lista_menace[-1]+1)
        print('MENACE ganhou!')        
    lista_empates.append(lista_empates[-1])


def empate(lista_de_listas):
    lista_jogador, lista_menace, lista_empates = lista_de_listas
    lista_jogador.append(lista_jogador[-1])
    lista_menace.append(lista_menace[-1])
    lista_empates.append(lista_empates[-1] + 1)
    print('Empate!')


# ------------------------------------ Classes        
class Caixinhas(pygame.sprite.Sprite):
    '''
    represent each position that can be chosen in the game. will change its value
    when clicked on.
    
    Args:
        mouse (object): player object (to get mouse/player identity O or X)
        num (int): box number/position 1-9

    Returns:
        sprites (list): list of pygame surfaces/sprites
    '''
    def __init__(self, mouse, num):
        super().__init__()
        self.value = 0
        self.sprites = get_sprites((19,19), 'files/assets/sprites/spr_caixinha.png')
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.mouse = mouse
        self.num = num
        delta = 220
        centerX, centerY = (455, 525)
        caixinhaDict = {
            1 : (centerX - delta, centerY - delta),
            2 : (centerX, centerY - delta),
            3 : (centerX + delta, centerY - delta),
            4 : (centerX - delta, centerY),
            5 : (centerX,centerY),
            6 : (centerX + delta, centerY),
            7 : (centerX - delta, centerY + delta),
            8 : (centerX, centerY + delta),
            9 : (centerX + delta, centerY + delta)
        }
        self.rect.center = caixinhaDict[self.num]
        
    def update(self, events, menace, grupo_caixas, lista_de_listas):
        if self.image == self.sprites[2] or self.image == self.sprites[3]:
            return
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)
        self.image = self.sprites[1] if hover else self.sprites[0]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hover:
                self.change_value(self.mouse.isX+1)
                menace.jogada(grupo_caixas, lista_de_listas)
        
            
    def change_value(self, valor):
        self.image = self.sprites[valor+1]
        self.value = valor


class OsAndXs(pygame.sprite.Sprite):
    def __init__(self, isX, xy=None):
        super().__init__()
        self.isX = isX
        if xy == None: return
        self.sprites = get_sprites((19,19), 'files/assets/sprites/spr_OsAndXs.png')
        self.image = self.sprites[isX]
        self.rect = self.image.get_rect()
        self.rect.center = list(xy)
                    
 
class Player(OsAndXs):
    def __init__(self, isX, xy=None):
        super().__init__(isX, xy)
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

     
class Menace(OsAndXs):
    def __init__(self, isX, xy=None, verbose=False):
        super().__init__(isX, xy)
        self.verbose = verbose
        self.menace = Jogador(isX+1)
    
    def jogada(self, grupo_caixas, lista_de_listas):
        estado_jogo = get_string(grupo_caixas)
        config = Configuracao(estado_jogo)
        if (
            (not config.check_vitoria(1))
            and (not config.check_vitoria(2))
            and (config.get_symmetry_id().count("0") > 0)
        ):
            config = self.menace.realizar_jogada(estado_jogo, self.verbose)
            atualizar_tela(grupo_caixas, estado_jogo, config)
        if config.check_vitoria(self.isX+1): vitoria(self.menace, lista_de_listas)
        elif config.check_vitoria((not self.isX)+1): vitoria('p', lista_de_listas, self.menace)
        elif config.get_symmetry_id().count("0") == 0: empate(lista_de_listas)
    

class CenaAnimada(pygame.sprite.Sprite):
    def __init__(self, x, y, isX):
        super().__init__()
        pass