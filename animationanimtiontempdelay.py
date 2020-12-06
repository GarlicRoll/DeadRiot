'''
Created on 3 мая 2020 г.

@author: 08k0708
Да, я заметил, что в названии модуля ошибка (перед защитой..)
'''

class Animation():
    #анимация, зависимая от действий
    def __init__(self, sprites, time = 100):
        self.sprites = sprites  #масиив со спрайтами
        self.time = time #время смены кадров
        self.workTime = 0 #общее время работы
        self.skipFrame = 0 #кол-во пропускаемых кадров
        self.currentFrame = 0 #текущая картинка
    def update(self, dt): #dt - промежуток времени работы анимации
        self.workTime += dt
        self.skipFrame = self.workTime // self.time #проверяем достаточно ли времени для смены кадров
        if self.skipFrame > 0: #проверяем прошёл ли кадр
            self.workTime = self.workTime % self.time
            self.currentFrame += self.skipFrame
            if self.currentFrame >= len(self.sprites):
                self.currentFrame = 0
    def get_sprite(self):
        #выдача спрайта
        return self.sprites[self.currentFrame]

class AnimationTemp(Animation):
    #временная анимация, проигрываемая определённое время
    def __init__(self, sprites, time):
        super(AnimationTemp, self).__init__(sprites, time)
        self.working = False
        self.workEnd = False
 
    def anim(self, dt):
        #анимация спрайта
        if self.working:
            
            if self.currentFrame < len(self.sprites)-1:
                self.workEnd = False#
                self.update(dt)
            else:
                self.working = False
                self.workEnd = True
                self.currentFrame = 0

class AnimationAttack(AnimationTemp):
    #нимация для атаки - нанесение урона после конца анимации
    def __init__(self, sprites, time):
        super(AnimationAttack, self).__init__(sprites, time)
    
    def set_parent(self, parent):
        #установка родителя анимации
        self.parent = parent
    
    def anim(self, dt):
        #анимация спрайта
        if self.working:
            
            if self.currentFrame < len(self.sprites)-1:
                self.workEnd = False#
                self.update(dt)
            else:
                self.working = False
                self.workEnd = True
                self.currentFrame = 0
                
                distx = abs(self.parent.rect.x - self.parent.target.rect.x)
                disty = abs(self.parent.rect.y - self.parent.target.rect.y)
                if distx < self.parent.rect.w//1.5:
                    if disty < self.parent.rect.h//1.5:
                        self.parent.target.hit(self.parent.damage)

class Delay():
    #временная задержка спрайта на экране
    def __init__(self, sprite, time = 150):
        self.sprite = sprite
        self.time = time
        self.workTime = 0
        self.working = False

    def update(self, dt):
        #обновление текущего спрайта
        if self.working:
            self.workTime += dt
            if self.workTime >= self.time:
                self.working = False
                self.workTime = 0
            
    def get_sprite(self):
        #выдача спрайта
        return self.sprite
    