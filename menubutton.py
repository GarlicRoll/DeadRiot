'''
Created on 3 мая 2020 г.

@author: 08k0708
'''

import pygame


from sprite import Sprite
from constants import WINDOW_W, WINDOW_H, SCREEN_W, SCREEN_H, BLOCK_SIZE

class Menu(Sprite):
    #меню
    def __init__(self, x, y, filename, parent):
        super(Menu, self).__init__(x, y, filename)
        self.rect.x = WINDOW_W//2 - self.rect.w//2
        self.rect.y = WINDOW_H//2 - self.rect.h//2 
        self.working = False
        self.parent = parent

        self.up = False #отпускание клавиши в меню
        self.down = False #нажатие в меню
        
        self.normal = pygame.image.load("gui/normal.png")
        self.hover = pygame.image.load("gui/hover.png")
        self.pressed = pygame.image.load("gui/pressed.png")
        
        self.offsety = self.normal.get_height() #отступ кнопок друг от друга по оси y 
        self.offsetx = self.normal.get_width()
        
        self.add_buttons()
        
    def activate(self):
        #активация/деактивация меню
        if self.working:
            self.working = False
            #self.parent.pause = False
        else:
            self.working = True
            #self.parent.pause = True
            
    def add_buttons(self):
        #добавление кнопок
        pass
        #self.exit_button = Button(self.rect.x + self.rect.w//2,self.rect.y + self.offsety*6, self.normal, self.hover, self.pressed, self)
        #self.exit_button.set_text(self.parent.texts[self.parent.language]["ButtonExit"])
        '''
        self.new_game_button = Button(self.rect.x + self.rect.w//2,self.rect.y + self.offsety*2, self.normal, self.hover, self.pressed, self)
        self.new_game_button.set_text(self.parent.texts[self.parent.language]["ButtonNewGame"])
        self.load_button = Button(self.rect.x + self.rect.w//2,self.rect.y + self.offsety*3, self.normal, self.hover, self.pressed, self)
        self.load_button.set_text(self.parent.texts[self.parent.language]["ButtonLoadGame"])
        '''
        
    def render(self, screen):
        #обновление спрайта
        screen.blit(self.bitmap, self.rect)
        #self.exit_button.render(screen)
        #self.new_game_button.render(screen)
        #self.load_button.render(screen)
        
        #описания, что делает каждая кнопка
        #if self.exit_button.up:
            #self.parent.running = False
        
        '''
        if self.new_game_button.up:
            self.new_game_button.up = False
            pygame.mouse.set_visible(False) #курсор скроется
            self.parent.new_game()
            self.activate()
            #self.parent.greeting.activate()
            
        if self.load_button.up:
            self.load_button.up = False
            pygame.mouse.set_visible(False) #курсор скроется
            self.parent.load_game()
            self.activate()
        '''
        
class Button(Sprite):
    #кнопка
    def __init__(self,x, y, filename, filename2, filename3, parent):
        super(Button , self).__init__(x, y, filename)
        self.bitmap2 = filename2
        self.bitmap3 = filename3
        self.parent = parent

        self.down = False #нажатие по клавише
        self.up = False #отпускание кнопки
        
        self.rect.x -= self.rect.w//2 #корректеровка по ширине (с исп. собственных размеров)
        
    def set_text(self, text, rgb = (150, 150, 0)):
        #установка текста для кнопки
        self.unicode = text
        self.text = pygame.font.Font(self.parent.parent.mainFont, 40).render(text, True, rgb)
        self.texth = self.text.get_height()
        self.textw = self.text.get_width()
    
    def set_color(self, rgb = (150, 150, 0)):
        #установка цвета для текста кнопки
        if rgb == "green": rgb = (25, 155, 25)
        if rgb == "gray": rgb = (155, 155, 155)
        self.text = pygame.font.Font(self.parent.parent.mainFont, 40).render(self.unicode, True, rgb)
    
    def check(self, screen):
        #логика нажатия кнопки 
        screen.blit(self.bitmap2, self.rect)
            
        self.up = False
            
        if self.parent.down:
            self.down = True
            screen.blit(self.bitmap3, self.rect)
                
        elif self.parent.up:
            self.up = True
    
    def render(self, screen):
        #обновление спрайта
        x,y = pygame.mouse.get_pos()
        if x > self.rect.x and x < self.rect.x + self.rect.w and y > self.rect.y and y < self.rect.y + self.rect.h: #наведение мыши на кнопку
            self.check(screen)
        else:
            screen.blit(self.bitmap, self.rect)
            
        
        screen.blit(self.text, (self.rect.x + self.rect.w//2 - self.textw//2, self.rect.y + self.rect.h//2 - self.texth//2))
            