'''
Created on 3 мая 2020 г.

@author: 08k0708
'''
from constants import WINDOW_W, WINDOW_H, SCREEN_W, SCREEN_H, BLOCK_SIZE

class Camera():
    #камера, следящая за целью
    def __init__(self, target):
        self.target = target #установка цели
    def update(self):
        #обновление камеры
        x = self.target.rect.x + self.target.rect.w//2
        x -= WINDOW_W//2
        
        y = self.target.rect.y + self.target.rect.h #отсчёт с верхнего, левого угла
        #y -= WINDOW_H - BLOCK_SIZE #в самый низ экрана, но чтобы былы видна земля
        
        w = WINDOW_W
        h = WINDOW_H
        if x < 0: x = 0
        elif x+WINDOW_W > SCREEN_W: x = SCREEN_W - WINDOW_W
        
        if y < 0: y = 0
        elif y+WINDOW_H > SCREEN_H: y = SCREEN_H - WINDOW_H

        return (x, y, w, h)