'''
Created on 10 мая 2020 г.

@author: Gleb
'''
from sprite import Sprite

class Spikes(Sprite):
    #шипы
    def __init__(self, x, y, filename, parent):
        super(Spikes, self).__init__(x, y, filename)
        self.parent = parent
        
    def collide(self):
        #взаимодействие
        entity = self.parent.player
        if self.rect.colliderect(entity.rect) and entity != self: #проверка столкновений
            entity.hit(entity.hp)