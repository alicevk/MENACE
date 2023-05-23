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
class OsAndXs(pygame.sprite.Sprite):
    def __init__(self, x, y, isX):
        super().__init__()
        self.sprites = get_sprites((20,20), 'files/sprites/spr_OsAndXs.png')
        self.image = self.sprites[0] if isX else self.sprites[1]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        
    def update(self):
         self.rect.center = pygame.mouse.get_pos()
         
class Caixinhas(pygame.sprite.Sprite):
    def __init__(self, on_click):
        super().__init__()
        self.sprites = get_sprites((20,20), 'files/sprites/spr_caixinha.png')
        self.normal = self.sprites[0]
        self.hover = self.sprites[1]
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.on_click = on_click
        self.rect.center = [460, 530]
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(mouse_pos)
        self.image = self.hover if hit else self.normal
