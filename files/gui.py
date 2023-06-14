"""
Este é o arquivo responsável por guardar todas as classes e funções utilizadas na
implementação da interface gráfica do MENACE!

:)
"""

from time import sleep as s
import pygame, pickle
from files.api import *

scale_factor = 10 # so every sprite has the same scale
brain_save_path = 'files/assets/brain.pickle'
DISPLAY_W, DISPLAY_H = 1280, 960
display_center = (DISPLAY_W/2, DISPLAY_H/2)
isX_constant = True


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


def get_bead(num):
    w, h = (6,4)
    x, y = ((num-1)*w,0)
    sheet = pygame.image.load('files/assets/sprites/spr_bead.png').convert_alpha()
    sheet.set_clip(pygame.Rect(x, y, w, h))
    sprite = sheet.subsurface(sheet.get_clip())
    sprite = pygame.transform.scale_by(sprite, scale_factor)
    return sprite


def get_string(grupo_caixas):
    saida = ''
    for caixa in grupo_caixas:
        saida += str(int(caixa.value))
    return saida


def atualizar_tela(grupo_caixas, jogada_antiga, jogada_atual, prob, grupo_probs):
    print(prob, grupo_probs)
    for n, sprite in enumerate(grupo_probs):
        probabilidade = prob[n]
        sprite.text = sprite.font.render(f'{probabilidade*100:.2f}%', True, (255,255,255))
    for caixa, valor_antigo, valor_atual in zip(grupo_caixas, jogada_antiga, jogada_atual.lista):
        if valor_antigo != str(valor_atual): caixa.change_value(valor_atual)
        
        
def vitoria(quem_ganhou, lista_de_listas, grupo_caixas, anim_grupo, pausado, menace=None):
    lista_jogador, lista_menace, lista_empates = lista_de_listas
    if quem_ganhou=='p':
        menace.atualizar_derrota()
        lista_jogador.append(lista_jogador[-1]+1)
        lista_menace.append(lista_menace[-1])
        # Animação:
        cena_voce_ganhou = CenaAnimada(display_center,(78, 20),'spr_voceVenceu.png')
        anim_grupo.add(cena_voce_ganhou)
        cena_voce_ganhou.animando = 20
        print('Você ganhou!')
    else:
        quem_ganhou.atualizar_vitoria()
        lista_jogador.append(lista_jogador[-1])
        lista_menace.append(lista_menace[-1]+1)
        # Animação:
        cena_voce_perdeu = CenaAnimada(display_center,(78, 20),'spr_vocePerdeu.png')
        anim_grupo.add(cena_voce_perdeu)
        cena_voce_perdeu.animando = 20
        print('MENACE ganhou!')        
    lista_empates.append(lista_empates[-1])
    s(1)
    reset_game(grupo_caixas)
    print(lista_de_listas)
    pausado[0] = True


def empate(lista_de_listas, grupo_caixas, anim_grupo, pausado):
    lista_jogador, lista_menace, lista_empates = lista_de_listas
    lista_jogador.append(lista_jogador[-1])
    lista_menace.append(lista_menace[-1])
    lista_empates.append(lista_empates[-1] + 1)
    # Animação:
    cena_empate = CenaAnimada(display_center,(78, 20),'spr_empate.png')
    anim_grupo.add(cena_empate)
    cena_empate.animando = 20
    print('Empate!')
    s(1)
    reset_game(grupo_caixas)
    print(lista_de_listas)
    pausado[0] = True


def reset_game(grupo_caixas):
    for caixa in grupo_caixas:
        caixa.change_value(0)
        

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
        
    def update(self, events, menace, grupo_caixas, lista_de_listas, anim_grupo, pausado, grupo_probs):
        if self.image == self.sprites[2] or self.image == self.sprites[3]:
            return
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)
        self.image = self.sprites[1] if hover else self.sprites[0]
        # Checa jogada:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hover:
                self.change_value(isX_constant+1)
                menace.jogada(grupo_caixas, lista_de_listas, anim_grupo, pausado, grupo_probs)
        
            
    def change_value(self, valor):
        if valor==0:
            self.image = self.sprites[0]
        else: self.image = self.sprites[valor+1]
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
    
    def jogada(self, grupo_caixas, lista_de_listas, anim_grupo, pausado, grupo_probs):
        # Jogada:
        estado_jogo = get_string(grupo_caixas)
        config = Configuracao(estado_jogo)
        if (
            (not config.check_vitoria(1))
            and (not config.check_vitoria(2))
            and (config.get_symmetry_id().count("0") > 0)
        ):
            config, prob = self.menace.realizar_jogada(estado_jogo, self.verbose, True)
            prob = prob.ravel()
            atualizar_tela(grupo_caixas, estado_jogo, config, prob, grupo_probs)
        # Check vitória, empate, etc.:
        if config.check_vitoria(self.isX+1): vitoria(self.menace, lista_de_listas, grupo_caixas, anim_grupo, pausado)
        elif config.check_vitoria((not self.isX)+1): vitoria('p', lista_de_listas, grupo_caixas, anim_grupo, pausado, self.menace)
        elif config.get_symmetry_id().count("0") == 0: empate(lista_de_listas, grupo_caixas, anim_grupo, pausado)
        else:
            # Animação:
            cena_embaralhando = CenaAnimada((2/5 * DISPLAY_W, DISPLAY_H/2),(70, 70),'spr_embaralhando.png')
            anim_grupo.add(cena_embaralhando)
            cena_embaralhando.animando = 15
    
    def save_pickle(self):
        with open(brain_save_path, 'wb') as handle:
            pickle.dump(self.menace.brain, handle, protocol=pickle.HIGHEST_PROTOCOL)
        

class CenaAnimada(pygame.sprite.Sprite):
    def __init__(self, xy, size, file):
        super().__init__()
        self.sprites = get_sprites(size, 'files/assets/sprites/'+file)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = list(xy)
        self.count = 0
        self.animando = 0
    
    def update(self, grupo_prob):
        if self.animando >= 0:
            buff = .2
            self.count += buff
            self.animando -= buff
        else: self.kill()
        if self.count >= len(self.sprites): self.count = 0
        self.image = self.sprites[int(self.count)]

                
class Probabilidades(pygame.sprite.Sprite):
    def __init__(self, text, num, display, font):
        super().__init__()
        self.font = font
        self.display = display
        self.num = num
        self.text = self.font.render(text, True, (255,255,255))
        self.prob_rect = self.text.get_rect()
        self.prob_rect.center = (3/4 * DISPLAY_W, DISPLAY_H/10 * num)
        self.image = get_bead(num)
        self.rect = self.image.get_rect()
        self.rect.center = (3/4 * DISPLAY_W - 70, DISPLAY_H/10 * num)
        
    def update(self):
        self.display.blit(self.text, self.prob_rect)
