import random
import numpy as np

class Field():
    def __init__(self, size, initValue = 0):
        self.size = w, h = size
        self.field = self._generateField(initValue)

    def getSize(self):
        return self.size

    def fillRandom(self, seed = None):
        if seed is not None:
            random.seed(seed)
        w, h = self.size
        r = np.random.rand(h, w)
        self.field = np.where(r > 0.5, 1, 0)

    def fillField(self, value):
        self.field = self._generateField(value)

    def setField(self, field):
        #TODO Fehlererkennung
        self.field = np.array(field)

    def getField(self):
        return self.field

    def setPixel(self, pos, state):
        x, y = pos
        self.field[y, x] = state

    def getPixel(self, pos):
        x, y = pos
        # print(str(pos)+' - '+str(self.field[x ,y]))
        return self.field[y, x]

    def update(self):
        w, h = self.size
        newField = [[self._newState((x,y)) for x in range(w)] for y in range(h)]
        self.field = np.array(newField)

    def loadFromFile(self, path):
        pass #TODO implement Method

    def print(self):
        print('Field: ')
        w, h = self.size
        for y in range(h):
            for x in range(w):
                pos = x, y
                print('#' if self.getPixel(pos)>0 else ' ', end='')
            print('')

    def _generateField(self, value):
        w, h = self.size
        field = np.full((h, w), value)
        return field

    def _newState(self, pos):
        state = self.getPixel(pos)
        neighbours = self._countNeighbours(pos)

        if(state == 0 and neighbours == 3):
            return 1 # wird geboren

        if(state == 1 and neighbours < 2):
            return 0 # stirbt an Einsamkeit

        if(state == 1 and neighbours > 3):
            return 0 # stirbt wegen Überbevölekrung

        return state

    def _countNeighbours(self, pos, throughWall = False):
        w, h = self.size
        x, y = pos

        if(throughWall):
            x1, x2 = x-1 if x-1>0 else x-1+w, (x+1 % w)+1
            y1, y2 = y-1 if y-1>0 else y-1+h, (y+1 % h)+1
            #TODO Wenn über Kante hinweg reinfolge falsch
        else:
            x1, x2 = max(x-1, 0), min(x+2, w)
            y1, y2 = max(y-1, 0), min(y+2, h)

        subField = self.field[y1:y2, x1:x2] #FIXME funktioniert nicht
        neighbours = np.sum(subField)
        neighbours -= self.getPixel(pos)
        return neighbours

