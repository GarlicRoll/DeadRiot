'''
Created on 3 мая 2020 г.

@author: 08k0708
'''
import pygame

from animationanimtiontempdelay import Delay
from collideobject import CollideObject
from sprite import Sprite

from constants import WINDOW_W, WINDOW_H, SCREEN_W, SCREEN_H, BLOCK_SIZE, SPEED


class Player(CollideObject):
    #игрок
    def __init__(self, x, y, filename, filename2, entities, enemies, parent):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.onGround = False
        self.leftStand = False #для правого или левого стэнда
        self.bitmap2 = pygame.image.load(filename2) #вторая статичная картинка
        self.bullets = [] #динамичекие объекты
        
        self.parent = parent
        
        self.damage = self.parent.types["Player"]["Damage"]
        
        self.entities = entities
        self.enemies = enemies
        
        self.kJump = 2
        self.kWalk = 1
        
        self.HP = self.parent.types["Player"]["HP"]  #величина для сравнения
        self.hp = self.HP
        
        self.hp0 = pygame.image.load("player/health/empty.png")
        self.hp1 = pygame.image.load("player/health/full.png")
        self.hpw = self.hp0.get_width()
        
        self.points = 0
        
        
        
        super(Player, self).__init__(x, y, filename) 
        
        self.rect.y -= self.rect.h #корректировка
        
    def initAnim(self, go_right, go_left):
        #инициализация анимаций движений вправо и влево
        self.go_left = go_left
        self.go_right = go_right
    
    def initShoot(self, shoot_right, shoot_left, effect, effect2):
        #инициализация анимаций выстрела вправо и влево
        self.shoot_left = Delay(pygame.image.load(shoot_left),200)
        self.shoot_right = Delay(pygame.image.load(shoot_right),200)
        
        self.effect_shoot = effect
        self.effect_shoot2 = effect2
        
    def initJump(self, jump_right, jump_left):
        #инициализация анимаций прыжка вправо и влево
        self.jump_left = Delay(pygame.image.load(jump_left))
        self.jump_right = Delay(pygame.image.load(jump_right))
    
    def initGet_damage(self, get_damage_right, get_damage_left, effect):
        #инициализация спрайтов получения урона справа и слева
        self.get_damage_left =  Delay(pygame.image.load(get_damage_left),400)
        self.get_damage_right = Delay(pygame.image.load(get_damage_right),400)
        
        self.effect_hit = effect
        
    def initDead(self, dead, effect):
        #инициализация спрайта смерти
        self.dead = pygame.image.load(dead)
        
        self.effect_dead = effect
    
    def initCoin(self, anim_coin):
        #инициализация спрайта монетки
        self.anim_coin = anim_coin
    
    def hit(self, damage):
        #получение урона
        self.hp -= damage
        if self.leftStand:
            self.get_damage_left.working = True
        else:
            self.get_damage_right.working = True
        if self.hp <= 0:
            self.death()
        else:
            self.effect_hit.play()
    
    def death(self):
        #смерть
        self.parent.game_over()
            
        self.effect_dead.play()
    
    def move(self, entities, dt):
        #движение
        if self.onGround == True:
            
            if self.right:
                #if self.rect.x+self.rect.width < SCREEN_W: self.vx = SPEED
                #else: self.vx = 0
                self.vx = SPEED*self.kWalk
                self.leftStand = False
                self.go_right.update(dt)
            
            if self.left: 
                #if self.rect.x > 0: self.vx = -SPEED
                #else: self.vx = 0
                self.vx = -SPEED*self.kWalk
                self.leftStand = True
                self.go_left.update(dt)
                
            if self.up:
                if self.rect.y > 0: self.vy = -SPEED*self.kJump
                else: self.vy = 0
                if self.leftStand:
                    self.jump_left.working = True
                else:
                    self.jump_right.working = True
             
            #if self.down:
                #if self.rect.y+self.rect.height < SCREEN_H: self.vy = SPEED
                #else: self.vy = 0
        
        for bullet in self.bullets:
            bullet.move(bullet, self.parent.collide_ent, self.parent.enemies)
        
        if not (self.left or self.right): self.vx = 0
        
        if self.leftStand:
            if self.rect.x <= 0: self.vx = 0
        else:
            if self.rect.x+self.rect.width >= SCREEN_W: self.vx = 0
        
        #if not (self.up or self.down): self.vy = 0
        
        self.shoot_left.update(dt)
        self.shoot_right.update(dt)
        self.jump_left.update(dt)
        self.jump_right.update(dt)
        self.get_damage_left.update(dt)
        self.get_damage_right.update(dt)
        
        self.anim_coin.update(dt)
        
        super(Player, self).move(entities)
    
    def render_points(self, screen):
        #обновление спрайтов для выведения на экран очков
        sprite = self.anim_coin.get_sprite()
        
        text = pygame.font.Font(self.parent.mainFont, 100).render(str(self.points), True, (150, 150, 0))
        screen.blit(sprite, (0, WINDOW_H//7))
        screen.blit(text, (WINDOW_W//7, WINDOW_H//7))
        
    def render_hp(self, screen):
        #обновление спрайта полоски жизней
        
        for heart in range(self.HP // 100):
            if self.hp > heart * 100:
                screen.blit(self.hp1, (self.hpw * (heart + 1), self.hpw)) #спрайт сердечка квадратный
            else:
                screen.blit(self.hp0, (self.hpw * (heart + 1), self.hpw))
        
    def render(self, screen): #рендер нашей анимации
        #обновление спрайта персонажа
        if not self.parent.pause and not self.parent.stop:

            if self.shoot_left.working: #1 - выстрел
                sprite = self.shoot_left.get_sprite()
            elif self.shoot_right.working:
                sprite = self.shoot_right.get_sprite()
            elif self.get_damage_left.working: #2 - получение урона
                sprite = self.get_damage_left.get_sprite()
            elif self.get_damage_right.working:
                sprite = self.get_damage_right.get_sprite()
            elif self.onGround == False or self.up: #3 - прыжок
                if self.leftStand: 
                    sprite = self.jump_left.get_sprite()
                else:
                    sprite = self.jump_right.get_sprite()
            else:
                if self.left: # 4 - ходьба
                    sprite = self.go_left.get_sprite()
                elif self.right:
                    sprite = self.go_right.get_sprite()
                else:
                    if self.leftStand:
                        sprite = self.bitmap2
                    else:
                        sprite = self.bitmap
        elif self.hp <= 0:
            sprite = self.dead
        else:
            if self.leftStand:
                sprite = self.bitmap2
            else:
                sprite = self.bitmap
            
            
        screen.blit(sprite, self.rect)
        
    def shoot(self):
        #выстрел
        if not self.shoot_left.working and not self.shoot_right.working and not (self.parent.stop or self.parent.pause):
            x = self.rect.x + self.rect.w//2
            y = self.rect.y + self.rect.h//2
            if self.damage > 100:
                file = "player/laser.png"
                self.effect_shoot2.play()#звук выстрела
            elif self.damage > 50:
                file = "player/bullet2.png"
                self.effect_shoot.play()#звук выстрела
            else:
                file = "player/bullet.png"
                self.effect_shoot.play()#звук выстрела
                
            
            
            if self.leftStand:
                self.shoot_left.working = True
            else:
                self.shoot_right.working = True
            
            self.bullets.append(Bullet(x, y, file, self.damage, self))
        
    def del_bullet(self, bullet):
        #удаление пули
        if bullet in self.bullets:
            self.bullets.remove(bullet)

class Bullet(Sprite):
    #пуля
    def __init__(self, x, y, filename, damage, parent):
        super(Bullet, self).__init__(x, y, filename)
        
        self.damage = damage
        self.parent = parent
        
        if self.parent.leftStand: #пуля летит туда, куда смотрит игрок
            self.vx = -10
        else:
            self.vx = 10
    
    def collide(self, entities, enemies): #разделение на обычные объекты и врагов пригодится здесь
        #соприкосновение с объектами
        for item in pygame.sprite.spritecollide(self, entities, None):
            self.parent.del_bullet(self) #удаление предмета через родителя (APP)
        for item in pygame.sprite.spritecollide(self, enemies, None):
            self.parent.del_bullet(self) #удаление предмета через родителя (APP)
            item.hit(self.damage)   
        
    def move(self, bullet, entities, enemies):
        #движение
        if self.rect.x <= 0 or self.rect.x >= SCREEN_W:
            self.parent.del_bullet(bullet)
        self.rect.x += self.vx
        self.collide(entities, enemies)
