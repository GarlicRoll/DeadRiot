'''
Created on 10 мая 2020 г.

@author: Gleb
'''
import pygame

from constants import WINDOW_H, BLOCK_SIZE
from animationanimtiontempdelay import AnimationTemp, Delay

class DialogWindow():
    #диалоговое окно
    def __init__(self, text, parent, num):
        self.num = num #кол-во доступных повторений
        self.count = 0 #кол-во повторений
        self.text = text
        self.parent = parent
        self.rect = pygame.font.Font(self.parent.mainFont, 50).render(self.text, True, (150, 150, 0)).get_rect()
        self.rect.y = WINDOW_H - BLOCK_SIZE
        sprites = []
        #textnew = []
        for sym in range(len(self.text)):
            sprites.append(pygame.font.Font(self.parent.mainFont, 50).render(self.text[:sym+1], True, (150, 150, 0)))
        
        self.textOutput = AnimationTemp(sprites, len(self.text) * 1 + 10)
        
        self.delay = Delay(sprites[-1], 1000)
        
        self.parent.dialog_windows.append(self)
        
    def activate(self):
        #вызов диалогового окна
        ok = True
        for win in self.parent.dialog_windows:
            if win.textOutput.working or win.delay.working:
                ok = False
        if ok:
            if self.count < self.num:
                self.count += 1
                self.textOutput.working = True
                
    
    def render(self, screen):
        #отрисовка
        #super(DialogWindow, self).render(screen)
        
        if self.textOutput.working:
            screen.blit(self.textOutput.get_sprite(), self.rect)
        if self.textOutput.workEnd:
            self.delay.working = True
            self.textOutput.workEnd = False
        if self.delay.working:
            screen.blit(self.delay.get_sprite(), self.rect)
        
        