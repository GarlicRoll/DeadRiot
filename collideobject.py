
from sprite import Sprite
from pygame import sprite

class CollideObject(Sprite):
    #объекты, которые учавствуют в сто-лкновениях
    def __init__(self, x, y, filename):
        super(CollideObject, self).__init__(x, y, filename)
        self.M = 10
        self.vx = 0
        self.vy = 0
    def collide(self, entities, vx, vy):
        #соприкосновение
        for entity in sprite.spritecollide(self, entities, None): #проверка столкновений
            if vx > 0:
                self.rect.right = entity.rect.left
            elif vx < 0:
                self.rect.left = entity.rect.right
            if vy > 0:
                self.rect.bottom = entity.rect.top
                self.onGround = True
                self.vy = 0 
            elif vy < 0:
                self.rect.top = entity.rect.bottom
                self.vy = 0
            
    def move(self, entities):
        #движение
        self.rect.x += self.vx
        self.collide(entities, self.vx, 0)
        self.rect.y += self.vy
        #два метода, чтобы объект полностью не прилип
        self.onGround = False
        self.collide(entities, 0, self.vy)
        