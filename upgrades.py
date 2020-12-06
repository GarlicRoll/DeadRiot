'''
Created on 17 мая 2020 г.

@author: Gleb
'''

import pygame
from menubutton import Menu, Button
from constants import WINDOW_W, WINDOW_H, BLOCK_SIZE

class Upgrades(Menu):
    #улучшения
    def __init__(self, x, y, filename, parent):
        super(Upgrades, self).__init__(x, y, filename, parent)
        
        #улучшения
        self.upgrade_damage1 = UpgradeDamage1(30, self.upgrade_damage1_button, self)
        self.parent.upgrades.append(self.upgrade_damage1)
        self.upgrade_damage2 = UpgradeDamage2(30, self.upgrade_damage2_button, self)
        self.parent.upgrades.append(self.upgrade_damage2)
        self.upgrade_speed = UpgradeSpeed(20, self.upgrade_speed_button, self)
        self.parent.upgrades.append(self.upgrade_speed)
        
        self.upgrade_hp1 = UpgradeHp1(20, self.upgrade_hp1_button, self)
        self.parent.upgrades.append(self.upgrade_hp1)
        self.upgrade_hp2 = UpgradeHp2(30, self.upgrade_hp2_button, self)
        self.parent.upgrades.append(self.upgrade_hp2)
        self.upgrade_jump = UpgradeJump(30, self.upgrade_jump_button, self)
        self.parent.upgrades.append(self.upgrade_jump)
        
    def add_buttons(self):
        #добавление кнопок
        #1 ветка
        self.upgrade_damage1_button = UpgradeButton(self.rect.x + self.rect.w//2 + self.offsetx//2, self.rect.y + self.offsety*2, self.normal, self.hover, self.pressed, self) # + self.rect.w//2
        self.upgrade_damage1_button.set_text(self.parent.texts[self.parent.language]["UpgradeDamage1"])
        
        self.upgrade_damage2_button = UpgradeButton(self.rect.x + self.rect.w//2 + self.offsetx//2, self.rect.y + self.offsety*4, self.normal, self.hover, self.pressed, self)
        self.upgrade_damage2_button.set_text(self.parent.texts[self.parent.language]["UpgradeDamage2"])
        
        self.upgrade_speed_button = UpgradeButton(self.rect.x + self.rect.w//2 + self.offsetx//2, self.rect.y + self.offsety*6, self.normal, self.hover, self.pressed, self)
        self.upgrade_speed_button.set_text(self.parent.texts[self.parent.language]["UpgradeSpeed"])

        #2 ветка
        self.upgrade_hp1_button = UpgradeButton(self.rect.x + self.rect.w//2 - self.offsetx//2, self.rect.y + self.offsety*2, self.normal, self.hover, self.pressed, self)
        self.upgrade_hp1_button.set_text(self.parent.texts[self.parent.language]["UpgradeHp1"])

        self.upgrade_hp2_button = UpgradeButton(self.rect.x + self.rect.w//2 - self.offsetx//2, self.rect.y + self.offsety*4, self.normal, self.hover, self.pressed, self)
        self.upgrade_hp2_button.set_text(self.parent.texts[self.parent.language]["UpgradeHp2"])

        self.upgrade_jump_button = UpgradeButton(self.rect.x + self.rect.w//2 - self.offsetx//2, self.rect.y + self.offsety*6, self.normal, self.hover, self.pressed, self)
        self.upgrade_jump_button.set_text(self.parent.texts[self.parent.language]["UpgradeJump"])
   
    def set_button_colors(self):
        self.upgrade_damage1_button.set_color()
        self.upgrade_damage2_button.set_color("gray")
        self.upgrade_speed_button.set_color("gray")
        
        self.upgrade_hp1_button.set_color()
        self.upgrade_hp2_button.set_color("gray")
        self.upgrade_jump_button.set_color("gray")
        
        
    def render(self, screen):
        #отрисовка
        screen.blit(self.bitmap, self.rect)
        self.upgrade_damage1_button.render(screen)
        self.upgrade_damage2_button.render(screen)
        self.upgrade_speed_button.render(screen)
        
        self.upgrade_hp1_button.render(screen)
        self.upgrade_hp2_button.render(screen)
        self.upgrade_jump_button.render(screen)
        
        #описания, что делает каждая кнопка
        #
        if self.upgrade_damage1_button.up:
            self.upgrade_damage1.buy()
            
        if self.upgrade_damage2_button.up:
            self.upgrade_damage2.buy()
            
        if self.upgrade_speed_button.up:
            self.upgrade_speed.buy()
            
        #
        if self.upgrade_hp1_button.up:
            self.upgrade_hp1.buy()
            
        if self.upgrade_hp2_button.up:
            self.upgrade_hp2.buy()
            
        if self.upgrade_jump_button.up:
            self.upgrade_jump.buy()
            
class UpgradeButton(Button):
    #кнопка для улучшений
    def __init__(self, x, y, filename, filename2, filename3, parent, points = 0):
        super(UpgradeButton, self).__init__(x, y, filename, filename2, filename3, parent)
        
        self.points = points
        
    def render(self, screen):
        #обновление спрайта
        x,y = pygame.mouse.get_pos()
        if x > self.rect.x and x < self.rect.x + self.rect.w and y > self.rect.y and y < self.rect.y + self.rect.h: #наведение мыши на кнопку
            
            text = pygame.font.Font(self.parent.parent.mainFont, 100).render(str(self.points), True, (150, 150, 0))# ради этого новый рендер
            screen.blit(text, (WINDOW_W - BLOCK_SIZE*2, WINDOW_H//7))#
            
            self.check(screen)

        else:
            screen.blit(self.bitmap, self.rect)
            
        
        screen.blit(self.text, (self.rect.x + self.rect.w//2 - self.textw//2, self.rect.y + self.rect.h//2 - self.texth//2))



class Upgrade():
    #общий класс для улучшений
    def __init__(self, points, button, parent):
        #self.target = target #тот, кому улучшаем характеристики
        self.button = button #кнопка, по которой покупается улучшение
        self.points = points
        self.button.points = self.points
        self.parent = parent
        
        self.bought = False #куплено ли улучшение
    
    def buy(self, noLimits = False):
        #получение улучшения
        if self.check() == False:
            if not noLimits:
                return False
        self.bought = True
        self.parent.parent.player.points -= self.points
        self.button.set_color("green")
        
    def check(self):
        #проверка хватит ли очков, не куплено ли улучшение и не закончена ли игра
        if not (self.parent.parent.player.points >= self.points and not self.bought and not self.parent.parent.stop):
            return False
'''
Улучшения
'''

class UpgradeDamage1(Upgrade):
    #первое увеличение урона
    
    def check(self):
        #проверка на последовательность
        if super(UpgradeDamage1, self).check() == False:
            return False
        elif self.parent.upgrade_hp1.bought:
            return False
    
    def buy(self, noLimits = False):
        #получение улучшения
        if not super(UpgradeDamage1, self).buy(noLimits) == False:
            self.parent.parent.player.damage += 50
            self.parent.upgrade_hp1_button.set_color("gray")
            self.parent.upgrade_damage2_button.set_color()

class UpgradeDamage2(Upgrade):
    #второе увеличение урона
    
    def check(self):
        #проверка на последовательность
        if super(UpgradeDamage2, self).check() == False:
            return False
        elif not self.parent.upgrade_damage1.bought:
            return False
    
    def buy(self, noLimits = False):
        #получение улучшения
        if not super(UpgradeDamage2, self).buy(noLimits) == False:
            self.parent.parent.player.damage += 50
            self.parent.upgrade_speed_button.set_color()
    
class UpgradeSpeed(Upgrade):
    #увеличение скорости
    
    def check(self):
        #проверка на последовательность
        if super(UpgradeSpeed, self).check() == False:
            return False
        elif not self.parent.upgrade_damage2.bought:
            return False
    
    def buy(self, noLimits = False):
        #получение улучшения
        if not super(UpgradeSpeed, self).buy(noLimits) == False:
            self.parent.parent.player.kWalk += 0.25

class UpgradeHp1(Upgrade):
    #первое увеличение здоровья
    
    def check(self):
        #проверка на последовательность
        if super(UpgradeHp1, self).check() == False:
            return False
        elif self.parent.upgrade_damage1.bought:
            return False
    
    def buy(self, noLimits = False):
        #получение улучшения
        if not super(UpgradeHp1, self).buy(noLimits) == False:
            self.parent.parent.player.HP += 100
            self.parent.parent.player.hp += 100
            self.parent.upgrade_damage1_button.set_color("gray")
            self.parent.upgrade_hp2_button.set_color()

class UpgradeHp2(Upgrade):
    #второе увеличение здоровья
    
    def check(self):
        #проверка на последовательность
        if super(UpgradeHp2, self).check() == False:
            return False
        elif not self.parent.upgrade_hp1.bought:
            return False
    
    def buy(self, noLimits = False):
        #получение улучшения
        if not super(UpgradeHp2, self).buy(noLimits) == False:
            self.parent.parent.player.HP += 100
            self.parent.parent.player.hp += 100
            self.parent.upgrade_jump_button.set_color()

class UpgradeJump(Upgrade):
    #увеличение прыжка
    
    def check(self):
        #проверка на последовательность
        if super(UpgradeJump, self).check() == False:
            return False
        elif not self.parent.upgrade_hp2.bought:
            return False
    
    def buy(self, noLimits = False):
        #получение улучшения
        if not super(UpgradeJump, self).buy(noLimits) == False:
            self.parent.parent.player.kJump += 0.5

    
                
                