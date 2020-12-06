'''
Created on 3 мая 2020 г.

@author: 08k0708
'''


from constants import  SCREEN_H, BLOCK_SIZE

import pygame
from collideobject import CollideObject


class Enemy(CollideObject):
    #класс врага
    def __init__(self, x, y, filename, filename2, parent, speed, hp, damage, points):
        super(Enemy, self).__init__(x, y, filename)
        
        self.parent = parent
        
        self.bitmap = filename

        self.bitmap2 = filename2
        
        
        self.hp = hp
        self.HP = self.hp
        
        self.damage = damage

        self.points = points

        self.speed = speed
        self.vx = 0
        self.leftStand = False
        
    def initSpawn(self, anim_spawn):
        #инициализация анимации спавна
        self.anim_spawn = anim_spawn
        
        self.anim_spawn.working = True
        
    def initAnim(self, go_right, go_left):
        #инициализация анимаций движений вправо и влево
        self.go_left = go_left
        self.go_right = go_right
    
    def initAttack(self, anim_attack_r, anim_attack_l, effect):
        #инициализация анимаций удара вправо и влево
        self.anim_attack_r = anim_attack_r
        self.anim_attack_l = anim_attack_l
        self.anim_attack_r.set_parent(self)
        self.anim_attack_l.set_parent(self)

        self.effect_damage = effect
    
    def initDead(self, anim_death_r, anim_death_l, effect_dead, effect_hit):
        #инициализация спрайта смерти
        self.anim_death_r = anim_death_r
        self.anim_death_l = anim_death_l
        
        self.effect_dead = effect_dead
        self.effect_hit = effect_hit

    def collide(self, entities, vx, vy): #collide был изменён в угоду удара при столкновении и отключения проверки на ось y
        for entity in pygame.sprite.spritecollide(self, entities, None): #проверка столкновений
            #if not (self.anim_attack_l.working or self.anim_attack_r.working):
                #self.effect_damage.play()
            if vx > 0:
                self.anim_attack_r.working = True #получается, что просчитываестя сразу и бег, и удар...
                self.rect.right = entity.rect.left
            elif vx < 0:
                self.anim_attack_l.working = True
                self.rect.left = entity.rect.right
                
    
    def set_target(self, target):
        #установка цели
        self.target = target

    def hit(self, damage):
        #получение урона
        self.hp -= damage
        if self.hp <= 0 and not(self.anim_death_l.working or self.anim_death_r.working): #чтобы монетки не начислялись при попадании в труп
            self.death()
        else:
            self.effect_hit.play()
    
    def death(self):
        #смерть врага
        if self.leftStand:
                self.anim_death_l.working = True
        else:
            self.anim_death_r.working = True
                
        self.target.points += self.points
        self.effect_dead.play()
        self.vx = 0
    
    def move(self,entities, dt):
        #движение
        #когда анимация появления кончится - ходим
        if self.anim_spawn.workEnd and not(self.anim_death_r.working or self.anim_death_l.working): 
            
            distx = self.rect.x - self.target.rect.x
            disty = abs(self.rect.y - self.target.rect.y)
            
            
            if distx > self.rect.w//2:
                self.vx = -self.speed
                self.go_left.update(dt)
                self.leftStand = True
            elif distx < -self.target.rect.w//2:
                self.vx = self.speed
                self.go_right.update(dt)
                self.leftStand = False
            else:
                
                self.vx = 0
                if disty < self.rect.h//1.5:
                    if self.leftStand and not self.anim_attack_l.working: #удар
                        self.anim_attack_l.working = True
                        #self.target.hit(self.damage)
                        self.effect_damage.play()
                    elif not self.leftStand and not self.anim_attack_r.working:
                        self.anim_attack_r.working = True 
                        #self.target.hit(self.damage)
                        self.effect_damage.play()

                    
        self.anim_death_r.anim(dt)
        self.anim_death_l.anim(dt)
        self.anim_attack_r.anim(dt)
        self.anim_attack_l.anim(dt)
        self.anim_spawn.anim(dt)
    
        #super(Enemy, self).move(entities)
        
        self.rect.x += self.vx
        self.collide(entities, self.vx, 0)
        
        if self.anim_death_l.workEnd == True:
            self.parent.enemies.remove(self)
        elif self.anim_death_r.workEnd == True:
            self.parent.enemies.remove(self)
        

        
    def render(self, screen):
        #обновление спрайта
        if self.anim_spawn.working:
            sprite = self.anim_spawn.get_sprite()
        elif self.hp > 0: #пока враг жив
            
            if self.anim_attack_l.working:
                sprite = self.anim_attack_l.get_sprite()
            elif self.anim_attack_r.working:
                sprite = self.anim_attack_r.get_sprite()
            elif self.vx < 0:
                    sprite = self.go_left.get_sprite()
            elif self.vx > 0:
                    sprite = self.go_right.get_sprite()
            else:
                if self.leftStand:
                    sprite = self.bitmap2
                else:
                    sprite = self.bitmap
            
        elif self.anim_death_l.working: 
            sprite = self.anim_death_l.get_sprite()
        elif self.anim_death_r.working:
            sprite = self.anim_death_r.get_sprite()
        
        
        rect = sprite.get_rect()
        self.rect.y = SCREEN_H - BLOCK_SIZE - rect.h #корректировка
        screen.blit(sprite, self.rect)

class Wave():
    #класс волны врагов
    def __init__(self, number, parent):
        self.number = number
        self.parent = parent
        
        for enemy in range(number):
            self.parent.create_enemy()
            
            
            