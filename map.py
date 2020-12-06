'''
Created on 26 июн. 2020 г.

@author: Gleb
'''

from random import choice

class Map():
    #карта
    def __init__(self):
        self.w = 40
        self.h = 5
        self.map = [[],[],[],[],[]]
        self.file = "map.txt"
    
    def write(self):
        file = self.file
        text = open(file, "w")
        map = ""
        first = True
        for h in self.map:
            if not first:
                map += "\n"
            for w in h:
                map += str(w)
            first = False
        text.write(map)
        text.close()
        
    def generate(self):
        #случайнаое создание карты
        for h in range(self.h):
            for w in range(self.w):
                if h == 0:
                    id = self.layer_0(w, h)
                elif h == 1:
                    id = self.layer_1(w, h)
                elif h == 2:
                    id = self.layer_2(w, h)
                elif h == 3:
                    id = self.layer_3(w, h)
                elif h == 4:
                    id = self.layer_4(w, h)
                self.map[h].append(id)
    
    def layer_0(self, w, h):
        #расчёт нулевого слоя
        if w > 1:
            if self.map[h][w-1] == 0 and self.map[h][w-2] == 0:
                id = choice([0, 0, 0, 5])
            else:
                id = 0
        else:
            id = 0
        return id
    
    def layer_1(self, w, h):
        #расчёт первого слоя
        id = 0
        return id
                
    def layer_2(self, w, h):
        #расчёт второго слоя
        if w > 1:
            if self.map[h][w-1] == 0 and self.map[h][w-2] == 0:
                id = choice([6, 3, 0, 0, 0, 0, 0])
            else:
                id = 0
        else:
            id = 0
        return id
    
    def layer_3(self, w, h):
        #расчёт третьего слоя
        if w > 1:
            if self.map[h][w-1] == 2 and self.map[h-1][w] != 3 and self.map[h-1][w - 1] != 3 and self.map[h-1][w] != 6:
                id = choice([2, 8, 0, 0])
            elif self.map[h][w-1] == 8:
                if self.map[h][w-2] == 8 and self.map[h-1][w] != 3 and self.map[h-1][w - 1] != 3:
                    id = choice([2, 8])
                elif self.map[h-1][w] != 3 and self.map[h-1][w - 1] != 3:
                    id = 8
                else:
                    id = 0
            elif self.map[h][w-1] != 7 and self.map[h][w-2] != 7 and self.map[h-1][w] != 3 and self.map[h-1][w - 1] != 3:
                id = choice([7, 4, 2, 0, 0, 0])
            else:
                id = 0
        else:
            id = 0
        
        return id
    
    def layer_4(self, w, h):
        #расчёт четвёртого слоя
        if self.map[h-1][w] == 2 or self.map[h-1][w] == 1:
            id = 1
        else:
            id = 2
        return id
    
m = Map()
m.generate()
m.write()
    
    