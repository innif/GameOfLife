import random
import numpy as np
from scipy.signal import convolve2d

class Field():
    def __init__(self, size, initValue = 0):
        self.size = w, h = size
        self.field = self._generateField(initValue)

    def getArray(self):
        return self.field

    def getSize(self):
        return self.size

    def fillRandom(self, seed = None):
        if seed is not None:
            random.seed(seed)
        w, h = self.size
        r = np.random.rand(h, w)
        self.field = np.where(r > 0.5, 1, 0).astype(np.int8)

    def fillField(self, value):
        self.field = self._generateField(value)

    def setField(self, field):
        #TODO Fehlererkennung
        self.field = np.array(field).astype(np.int8)

    def placeFigure(self, figure, offset = (0,0)):
        #TODO Fehlererkennung
        h, w = np.array(figure).shape
        figure = np.array(figure)
        x1, y1 = offset
        x2, y2 = x1+w, y1+h

        #deal with offsets below 0:
        if x1 < 0:
            figure = figure[:, -x1:w]
            x1 = 0

        if y1 < 0:
            figure = figure[-y1:h, :]
            y1 = 0

        #TODO deal with offsets above h/w

        self.field[y1:y2, x1:x2] = figure

    def getField(self):
        return self.field

    def getPixel(self, pos):
        x, y = pos
        # print(str(pos)+' - '+str(self.field[x ,y]))
        return self.field[y, x]

    def update(self):
        neighboursCount = self._neighboursMatrix()
        survivorsA = neighboursCount >= 2
        survivorsB = neighboursCount <= 3
        self.field = self.field*survivorsA*survivorsB
        self.field = np.where(neighboursCount == 3, 1, self.field)

    def loadFromFile(self, path):
        #TODO
        pass

    def print(self):
        print('Field: ')
        w, h = self.size
        for y in range(h):
            for x in range(w):
                pos = x, y
                print('#' if self.getPixel(pos)>0 else ' ', end='')
            print('')
            
    def _neighboursMatrix(self):
        kernel = np.array(
            [
                [1,1,1],
                [1,0,1],
                [1,1,1],
            ]
        )
        neighboursCount = convolve2d(self.field, kernel, mode='same', boundary='wrap')
        return neighboursCount

    def _setPixel(self, pos, state):
        x, y = pos
        self.field[y, x] = state

    def _generateField(self, value):
        w, h = self.size
        field = np.full((h, w), value).astype(np.int8)
        return field

