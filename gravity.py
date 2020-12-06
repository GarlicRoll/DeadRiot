'''
Created on 3 мая 2020 г.

@author: 08k0708
'''



class Gravity():
    #гравитация
    def __init__(self, g):
        self.g = g
    def force(self, entities):
        #ускорение свободного падения
        for entity in entities:
            entity.vy += self.g*entity.M