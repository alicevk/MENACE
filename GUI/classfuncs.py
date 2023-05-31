"""
Este é o arquivo responsável por guardar todas as classes e funções utilizadas na implementação do
MENACE!

:)
"""

import pygame
scale_factor = 10

# ------------------------------------ Functions
def get_sprites(size, file):
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
    def __init__(self, mouse, num):
        super().__init__()
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
                saida = self.change_value()
                return saida
        
            
    def change_value(self):
        '''
        Returns:
            box_num: in which box (1 to 9) the value was changed
            
            player_num: whether the 'player' who changed the value is an O or X
            (O being player #1 and X player #2)
        '''
        self.image = self.sprites[2] if self.mouse.isX else self.sprites[3]
        box_num = self.num
        player_num = self.mouse.isX+1
        return box_num, player_num


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
        
    def update(self):#, events, grupo):
        self.rect.center = pygame.mouse.get_pos()

     
# class Menace(OsAndXs):
#     def __init__(self, x, y, isX):
#         super().__init__(x, y, isX)


class CenaAnimada(pygame.sprite.Sprite):
    def __init__(self, x, y, isX):
        super().__init__()
        pass