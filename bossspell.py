'''
Created on 10 мая 2020 г.

@author: Gleb
'''

from enemywave import Enemy
from random import randint
from sprite import Sprite

from constants import BLOCK_SIZE, SCREEN_H

class Boss(Enemy):
    #босс
    def __init__(self, x, y, filename, filename2, parent, speed, hp, damage, points):
        super(Boss, self).__init__(x, y, filename, filename2, parent, speed, hp, damage, points)
        
        
    def set_spell(self, spell):
        #установка заклинания
        self.spell = spell
        self.spell.set_target(self.target)
        
    def render(self, screen):
        #отрисовка
        super(Boss, self).render(screen)
        
        #условия для использования заклинания
        if self.hp <= self.HP//2:
            if not (self.spell.anim_hit_r.working or self.spell.anim_hit_l.working):
                if self.leftStand:
                    self.spell.rect.x = self.rect.x - BLOCK_SIZE*3
                else:
                    self.spell.rect.x = self.rect.x + self.rect.w + BLOCK_SIZE*3
                
                self.spell.barrier = False
                self.spell.collide(self.parent.collide_ent, self.parent.enemies)
                if self.spell.barrier == False:
                    self.spell.activate()
                
        if self.spell.anim_hit_r.working or self.spell.anim_hit_l.working:
            self.spell.render(screen)
        
            
        
class Spell(Sprite):
    #заклинание
    def __init__(self, x, y, filename, damage, parent):
        super(Spell, self).__init__(x, y, filename)
        self.damage = damage
        self.parent = parent
        self.rect.y = SCREEN_H - BLOCK_SIZE - self.rect.h
        self.barrier = False
    
    def set_target(self, target):
        self.target = target
    
    def initAnim(self, anim_hit_r, anim_hit_l, effect):
        #инициализация анимации использования заклинания
        self.anim_hit_l = anim_hit_l
        self.anim_hit_r = anim_hit_r
        self.anim_hit_l.set_parent(self)
        self.anim_hit_r.set_parent(self)
        self.effect = effect
    
    def activate(self):
        #активация заклинания
        #self.rect.x = x
        if randint(0,1) == 0:
            self.anim_hit_l.working = True
        else:
            self.anim_hit_r.working = True
            
        self.effect.play()
            
    def collide(self, blocks, enemies):
        #взаимодейтвие звклинания с целью
        
        for block in blocks: #проверка со всеми блоками, лучше конечно это оптимизировать
            if self.rect.colliderect(block.rect): #проверка столкновений
                self.barrier = True
                break
        
        if not self.barrier:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect): #проверка столкновений
                    enemy.hit(self.damage)
                    
            #if self.rect.colliderect(target.rect): #проверка столкновений
                #target.hit(self.damage)
            
    
    def render(self, screen):
        #отрисовка
        if self.anim_hit_l.working:
            sprite = self.anim_hit_l.get_sprite()
        elif self.anim_hit_r.working:
            sprite = self.anim_hit_r.get_sprite()
        
        screen.blit(sprite, self.rect)
        
        
        