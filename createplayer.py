'''
Created on 12 авг. 2020 г.

@author: Gleb
'''

from playerbullet import Player
from animationanimtiontempdelay import Animation
from camera import Camera

from constants import BLOCK_SIZE, SCREEN_H, VOLUME

import pygame

def create_player(self):
        #создание игрока
        self.player = Player(BLOCK_SIZE, SCREEN_H - BLOCK_SIZE, self.types["Player"]["Idle_r"],  self.types["Player"]["Idle_l"], self.collide_ent, self.enemies, self) 
        self.gravity_ent.append(self.player)
        #анимация ходьбы влево
        sprites = []
        sprite = pygame.image.load(self.types["Player"]["Anim_go_l"][0])
        w = sprite.get_width()//int(self.types["Player"]["Anim_go_l"][1])
        h = sprite.get_height()
        for x in range(self.types["Player"]["Anim_go_l"][1]):
            sprites.append(sprite.subsurface(x * w, 0, w, h)) #разрезаем картинку
        go_left = Animation(sprites, 50) 
        
        #анимация ходьбы вправо
        sprites = []
        sprite = pygame.image.load(self.types["Player"]["Anim_go_r"][0])
        w = sprite.get_width()//int(self.types["Player"]["Anim_go_r"][1])
        h = sprite.get_height()
        for x in range(self.types["Player"]["Anim_go_r"][1]):
            sprites.append(sprite.subsurface(x * w, 0, w, h)) #разрезаем картинку
        go_right = Animation(sprites, 50) 
        
        self.player.initAnim(go_right, go_left)
        
        sprites = []
        sprite = pygame.image.load("player/coin.png")
        for x in range(8):
            sprites.append(sprite.subsurface(x * 120, 0, 120, 120)) #разрезаем картинку
        anim_coin = Animation(sprites, 100)
        
        self.player.initCoin(anim_coin)
        
        #анимация стрельбы
        shoot_left = self.types["Player"]["Anim_attack_l"]
        shoot_right = self.types["Player"]["Anim_attack_r"]
        
        effect = pygame.mixer.Sound('player/pistol.ogg')
        effect.set_volume(VOLUME)
        effect2 = pygame.mixer.Sound('player/laser.ogg')
        effect2.set_volume(VOLUME)
        
        self.player.initShoot(shoot_right, shoot_left, effect, effect2)
        
        #анимация прыжка
        jump_left = self.types["Player"]["Anim_jump_l"]
        jump_right = self.types["Player"]["Anim_jump_r"]
        
        self.player.initJump(jump_right, jump_left)
        
        #анимация получения урона
        get_damage_left = "player/hit_l.png"
        get_damage_right = "player/hit_r.png"
        
        effect = pygame.mixer.Sound('player/damage.ogg')
        effect.set_volume(VOLUME)
        
        self.player.initGet_damage(get_damage_right, get_damage_left, effect)
        
        #аниамция смерти
        dead = self.types["Player"]["Anim_death"]
        
        effect = pygame.mixer.Sound('player/death.ogg')
        effect.set_volume(VOLUME)
        
        self.player.initDead(dead, effect)
        
        #камера
        self.look = Camera(self.player)
        