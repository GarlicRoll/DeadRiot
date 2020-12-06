'''
Created on 21 мая 2020 г.

@author: Gleb
'''
import pygame

from constants import BLOCK_SIZE
from animationanimtiontempdelay import Animation, AnimationTemp, AnimationAttack

from json import loads

def initAnims(self):
    #инициализация анимаций

    text = open("types.json")
    self.types = loads(text.read())
    text.close()

        
    for type in range(len(self.types["Mob"])):
        
        self.types["Mob"][type]["Idle_l"] =  pygame.image.load(self.types["Mob"][type]["Idle_l"])
        self.k = self.types["Mob"][type]["Idle_l"].get_height()/BLOCK_SIZE/2
        sprite = self.types["Mob"][type]["Idle_l"]

        sprite.convert_alpha()
            
            
        sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k))) #чтобы сделать как прежде нужно вернуть целочисленное деление
        self.types["Mob"][type]["Idle_l"] = sprite
            
        self.types["Mob"][type]["Idle_r"] =  pygame.image.load(self.types["Mob"][type]["Idle_r"])
            
        sprite = self.types["Mob"][type]["Idle_r"]

        sprite.convert_alpha()
            
        sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k)))
        self.types["Mob"][type]["Idle_r"] = sprite

        #временные анимации (класс AnimationTemp)
        for anim in self.types["Mob"][type]["Anims"]:
            sprites = []
            sprite = pygame.image.load(self.types["Mob"][type]["Anims"][anim][0])
                
            sprite.convert_alpha()
    
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k)))
     
            w = sprite.get_width()/self.types["Mob"][type]["Anims"][anim][1]
            h = sprite.get_height()
    
            for i in range(int(self.types["Mob"][type]["Anims"][anim][1])):
                sprites.append(sprite.subsurface((i * w), 0, w, h)) #разрезаем картинку
            self.types["Mob"][type]["Anims"][anim] = AnimationTemp(sprites, 100)
            
        #attack_r
        anim = self.types["Mob"][type]["Anim_attack_r"]
        sprites = []
        sprite = pygame.image.load(anim[0])
            
        sprite.convert_alpha()
            
        sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k)))
            
        w = sprite.get_width()/self.types["Mob"][type]["Anim_attack_r"][1]
        h = sprite.get_height()
            
        for i in range(int(anim[1])):
            sprites.append(sprite.subsurface((i * w), 0, w, h)) #разрезаем картинку
        self.types["Mob"][type]["Anim_attack_r"] = AnimationAttack(sprites, 100)
        
        #attack_l
        anim = self.types["Mob"][type]["Anim_attack_l"]
        sprites = []
        sprite = pygame.image.load(anim[0])
            
        sprite.convert_alpha()
            
        sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k)))
            
        w = sprite.get_width()/self.types["Mob"][type]["Anim_attack_l"][1]
        h = sprite.get_height()
            
        for i in range(int(anim[1])):
            sprites.append(sprite.subsurface((i * w), 0, w, h)) #разрезаем картинку
        self.types["Mob"][type]["Anim_attack_l"] = AnimationAttack(sprites, 100)
        
        #go_r
        anim = self.types["Mob"][type]["Anim_go_r"]
        sprites = []
        sprite = pygame.image.load(anim[0])
            
        sprite.convert_alpha()
            
        sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k)))
            
        w = sprite.get_width()/self.types["Mob"][type]["Anim_go_r"][1]
        h = sprite.get_height()
            
        for i in range(int(anim[1])):
            sprites.append(sprite.subsurface((i * w), 0, w, h)) #разрезаем картинку
        self.types["Mob"][type]["Anim_go_r"] = Animation(sprites, 100)
            
        #go_l
        anim = self.types["Mob"][type]["Anim_go_l"]
        
        sprites = []
        sprite = pygame.image.load(anim[0])
            
        sprite.convert_alpha()
            
        sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k)))
            
        w = sprite.get_width()/self.types["Mob"][type]["Anim_go_l"][1]
        h = sprite.get_height()
            
        for i in range(int(anim[1])):
            sprites.append(sprite.subsurface((i * w), 0, w, h)) #разрезаем картинку
        self.types["Mob"][type]["Anim_go_l"] = Animation(sprites, 100)
        
    for type in range(len(self.types["Spell"])):
        #заклинания
            
        self.types["Spell"][type]["Idle"] =  pygame.image.load(self.types["Spell"][type]["Idle"])
        sprite = self.types["Spell"][type]["Idle"]

        sprite.convert_alpha()
    
        sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k))) #чтобы сделать как прежде нужно вернуть целочисленное деление
        self.types["Spell"][type]["Idle"] = sprite

        for anim in self.types["Spell"][type]["Anims"]:
            sprites = []
            sprite = pygame.image.load(self.types["Spell"][type]["Anims"][anim][0])
                
            sprite.convert_alpha()
    
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width()/self.k), int(sprite.get_height()/self.k)))
     
            w = sprite.get_width()/self.types["Spell"][type]["Anims"][anim][1]
            h = sprite.get_height()
    
            for i in range(int(self.types["Spell"][type]["Anims"][anim][1])):
                sprites.append(sprite.subsurface((i * w), 0, w, h)) #разрезаем картинку
            self.types["Spell"][type]["Anims"][anim] = AnimationAttack(sprites, 100)
        
    