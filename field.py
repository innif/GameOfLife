import random
import numpy as np
from scipy.signal import convolve2d
import logging

class Field():
    def __init__(self, size = (0,0), initValue = 0):
        self.size = w, h = size
        self.field = self._generateField(initValue)

    def getArray(self):
        return self.field

    def getSize(self):
        return self.size

    def fillRandom(self, seed = None):
        if seed is not None:
            np.random.seed(seed)
        w, h = self.size
        r = np.random.rand(h, w)
        self.field = np.where(r > 0.5, 1, 0).astype(np.int8)

    def fillField(self, value):
        self.field = self._generateField(value)

    def setField(self, field):
        ''' sets the field to the given value. 0 means dead, everything else means alive (should be a byte-number)
            
            field -> two dimensional list
        '''
        newField = self._toFieldArray(field)
        if newField is None:
            logging.warning('setField() failed')
            return
        self.size = newField.shape # update field size
        self.size = self.size[1], self.size[0]
        self.field = newField

    def placeFigure(self, figure, offset = (0,0)):
        ''' places a figure at the given offset
        
        figure -> anything that can be converted to a numpy array '''

        figure = self._toFieldArray(figure)
        if figure is None:
            logging.warning('placeFigure() failed')
            return
        hFig, wFig = figure.shape[:2] 
        x1, y1 = offset
        w, h = self.size

        for x in range(wFig):
            for y in range(hFig):
                self.field[(y1+y)%h, (x1+x)%w] = figure[y, x]

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
        f = open(path, 'r')
        lines = f.readlines()
        w = len(lines[0])-1 # länge des ersten Strings -1, da jede Zeile auf \n endet

        field = []
        for l in lines:
            l = [char for char in l[0:w]]
            field.append(l)

        field = np.array(field)
        field = np.where(field == '#', 1, 0)
        self.setField(field)

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

    def _toFieldArray(self, listInput):
        try:
            newField = np.array(listInput).astype(np.int8) # Input is converted to numpy array
        except ValueError:
            logging.warning('failed converting listInput to numpy array')
            return None
        
        if len(newField.shape) is not 2: # reads number of dimensions of numpy array
            logging.warning('listInput dimension has wrong shape. It should be a two dimensional List.')
            return None

        newField = np.where(newField == 0, 0, 1)
        return newField

