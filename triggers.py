'''
Created on 3 авг. 2020 г.

@author: Gleb
'''
from constants import BLOCK_SIZE, SCREEN_H, SCREEN_W
from collideobject import CollideObject


#триггеры различных событий
#запускается из App
def triggers(self):
    if self.level == 1: #первый уровень
        self.msg11.activate() #вступление
        
        if self.player.rect.x >= 18 * BLOCK_SIZE and self.player.rect.y >= SCREEN_H//2:
            self.msg12.activate() #первая проблема
        if self.player.rect.x >= 23 * BLOCK_SIZE and self.player.rect.x <= 25 * BLOCK_SIZE and self.player.rect.y >= SCREEN_H - BLOCK_SIZE * 3:
            self.msg13.activate() #для внимательных
        if self.player.rect.x >= 53 * BLOCK_SIZE:
            self.msg14.activate() #завязка
        if self.player.rect.x >= 56 * BLOCK_SIZE:
            self.level = 2
            self.map = "level2.txt"
            self.create_map(self.map)
            self.player.rect.x = BLOCK_SIZE
            
    if self.level == 2: #второй уровень
        self.msg21.activate() #шум
        
        if self.player.rect.x >= SCREEN_W//2:
            if self.msg22.count == 0:
                self.next_wave()
                self.game_channel.stop()
            self.msg22.activate() #встреча с мертвецами
        
        if self.waves == 3 and self.enemies == []:
            if self.msg23.count == 0:
                self.game_channel.stop()
            self.msg23.activate() #продолжение поисков
        
        if self.msg23.count == 1:
            if self.player.rect.x < BLOCK_SIZE * 4:
                self.level = 3
                self.map = "level3.txt"
                self.create_map(self.map)
                self.player.rect.y -= BLOCK_SIZE * 3
                self.waves = 0
    
    if self.level == 3: #третий уровень
        self.msg31.activate() #интересная находка
        
        if self.player.rect.x >= BLOCK_SIZE * 37 and self.player.rect.y > SCREEN_H - BLOCK_SIZE * 4:
            if self.msg32.count == 0:
                self.create_enemy(type = 1, x = BLOCK_SIZE * 40)
            self.msg32.activate() #случайный зомби
        
        if self.player.rect.x >= SCREEN_W - BLOCK_SIZE * 7:
            self.msg33.activate() #выход наружу
    
        if self.player.rect.x >= SCREEN_W - BLOCK_SIZE * 2 and self.enemies == []:
            self.level = 4
            self.map = "level4.txt"
            self.create_map(self.map)
            
            self.gate = CollideObject(SCREEN_W - BLOCK_SIZE * 10, SCREEN_H - BLOCK_SIZE * 3, "tiles/stone.png")
            self.collide_ent.append(self.gate) #камень с отдельным именем, чтобы убрать его позже
            
            self.player.rect.y += BLOCK_SIZE * 3
            self.player.rect.x = BLOCK_SIZE * 8
    
    if self.level == 4: #четвёртый уровень

        if self.player.rect.x >= SCREEN_W//2:
            if self.msg41.count == 0:
                self.next_wave()
                self.game_channel.stop()
            self.msg41.activate() #кладбище и небольшое сражение
            
        if self.waves == 5 and self.enemies == []:
            if self.msg42.count == 0:
                self.game_channel.stop()
            self.msg42.activate() #кульминация

            if not self.msg42.textOutput.working and not self.msg42.delay.working and self.msg42.count > 0:
                if self.msg43.count == 0:
                    self.create_enemy(type = 4, boss = True, x = SCREEN_W - BLOCK_SIZE * 8)
                self.msg43.activate()
        
        #ГГ подходит к дедушке
        if (self.msg43.textOutput.working or self.msg44.textOutput.working or self.msg43.delay.working or self.msg44.delay.working):
            if self.player.rect.x < SCREEN_W - BLOCK_SIZE * 12:
                self.player.right = True
                self.player.left = False
                self.player.up = False
            else:
                self.player.right = False
                self.player.left = False
                self.player.up = False
        
            
                
        if not self.msg43.textOutput.working and not self.msg43.delay.working and self.msg43.count > 0:
            self.msg44.activate() #развязка
            
        if not self.msg44.textOutput.working and not self.msg44.delay.working and self.msg44.count > 0 and self.waves == 5:
            self.collide_ent.remove(self.gate)
            self.next_wave()
                
        if self.waves == 6:
           
            if self.enemies == []:
                self.msg45.activate() #конец
            
                if not self.msg45.textOutput.working:
                    self.battle_music.stop()
                    self.end_music.play(-1, fade_ms = 4000)
                    self.win()
            
        
        
        
        
        
    
    
    
        
            
            