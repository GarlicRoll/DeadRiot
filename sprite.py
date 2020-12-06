'''
Created on 3 мая 2020 г.

@author: 08k0708
'''

import pygame

class Sprite():
    #спрайт
    def __init__(self, x, y, filename, alpha = True):
        if type(filename) == type(" ") and alpha == False:
            self.bitmap = pygame.image.load(filename)
            self.bitmap = self.bitmap.convert() #быстродействие
        elif type(filename) == type(" "):
            self.bitmap = pygame.image.load(filename)
            self.bitmap = self.bitmap.convert_alpha() #быстродействие
        else:
            self.bitmap = filename
        self.rect = self.bitmap.get_rect()
        self.rect.x = x
        self.rect.y = y
        #self.bitmap.set_colorkey((255, 255, 255))
    def render(self, screen):
        #обновление спрайта
        screen.blit(self.bitmap, self.rect)