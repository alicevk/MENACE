"""
Este é o arquivo responsável por guardar todas as classes e funções utilizadas na
implementação da interface gráfica do MENACE!

:)
"""

import pygame
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
        self.sprites = get_sprites((19,19), 'GUI/files/sprites/spr_caixinha.png')
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
        
    def update(self, events):
        if self.image == self.sprites[2] or self.image == self.sprites[3]:
            return
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)
        self.image = self.sprites[1] if hover else self.sprites[0]
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hover:
                return self.change_value(2) if self.mouse.isX else self.change_value(1)
        
            
    def change_value(self, valor):
        self.image = self.sprites[valor+1]
        self.value = valor


class OsAndXs(pygame.sprite.Sprite):

    def __init__(self, x, y, isX):
        super().__init__()
        self.isX = isX
        self.sprites = get_sprites((19,19), 'GUI/files/sprites/spr_OsAndXs.png')
        self.image = self.sprites[0] if self.isX else self.sprites[1]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
            
 
class Player(OsAndXs):
    def __init__(self, x, y, isX):
        super().__init__(x, y, isX)
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

     
# class Menace(OsAndXs):

class CenaAnimada(pygame.sprite.Sprite):
    def __init__(self, x, y, isX):
        super().__init__()
        pass