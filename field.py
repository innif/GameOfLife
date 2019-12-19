import random
import numpy as np
from scipy.signal import convolve2d
import logging

class Field():
    def __init__(self, size = (0,0), initValue = 0):
        self.size_ = size
        self.field_ = self._generateField(initValue)

    def getArray(self):
        return self.field_

    def getSize(self):
        return self.size_

    def fillRandom(self, seed = None):
        if seed is not None:
            np.random.seed(seed)
        w, h = self.size_
        r = np.random.rand(h, w)
        self.field_ = np.where(r > 0.5, 1, 0).astype(np.int8)

    def fillField(self, value):
        self.field_ = self._generateField(value)

    def setField(self, field):
        ''' sets the field to the given value. 0 means dead, everything else means alive (should be a byte-number)
            
            field -> two dimensional list
        '''
        newField = self._toFieldArray(field)
        if newField is None:
            logging.warning('setField() failed')
            return
        self.size_ = newField.shape # update field size
        self.size_ = self.size_[1], self.size_[0]
        self.field_ = newField

    def placeFigure(self, figure, offset = (0,0)):
        ''' places a figure at the given offset
        
        figure -> anything that can be converted to a numpy array '''

        figure = self._toFieldArray(figure)
        if figure is None:
            logging.warning('placeFigure() failed')
            return
        
        self._placeNumpyArray(figure, offset)

    def placeTemplate(self, template, offset = (0,0)):
        ''' places an object of the template class at the given offset
        
        figure -> anything that can be converted to a numpy array '''
        self.placePointlist(template._pointlist, offset=offset)

    def placePointlist(self, pointlist, offset=(0,0)):
        xOff, yOff = offset
        w, h = self.size_
        for p in pointlist:
            x, y = p
            place = (y+yOff)%h, (x+xOff)%w
            self.field_[place] = 1


    def getField(self):
        return self.field_

    def getPixel(self, pos):
        x, y = pos
        # print(str(pos)+' - '+str(self.field_[x ,y]))
        return self.field_[y, x]

    def update(self):
        neighboursCount = self._neighboursMatrix()
        survivorsA = neighboursCount >= 2
        survivorsB = neighboursCount <= 3
        self.field_ = self.field_*survivorsA*survivorsB
        self.field_ = np.where(neighboursCount == 3, 1, self.field_)

    def loadFromFile(self, path):
        f = open(path, 'r')
        lines = f.readlines()
        w = len(lines[0])-1 # laenge des ersten Strings -1, da jede Zeile auf \n endet

        field = []
        for l in lines:
            l = [char for char in l[0:w]]
            field.append(l)

        field = np.array(field)
        field = np.where(field == '#', 1, 0)
        self.setField(field)

    def print(self):
        print('Field: ')
        w, h = self.size_
        for y in range(h):
            for x in range(w):
                pos = x, y
                print('#' if self.getPixel(pos)>0 else ' ', end='')
            print('')

    def _placeNumpyArray(self, array, offset):
        hFig, wFig = array.shape[:2] 
        x1, y1 = offset
        w, h = self.size_

        for x in range(wFig):
            for y in range(hFig):
                self.field_[(y1+y)%h, (x1+x)%w] += array[y, x]
            
    def _neighboursMatrix(self):
        kernel = np.array(
            [
                [1,1,1],
                [1,0,1],
                [1,1,1],
            ]
        )
        neighboursCount = convolve2d(self.field_, kernel, mode='same', boundary='wrap')
        return neighboursCount

    def _setPixel(self, pos, state):
        x, y = pos
        self.field_[y, x] = state

    def _generateField(self, value):
        w, h = self.size_
        field = np.full((h, w), value).astype(np.int8)
        return field

    def _toFieldArray(self, listInput):
        try:
            newField = np.array(listInput).astype(np.int8) # Input is converted to numpy array
        except ValueError:
            logging.warning('failed converting listInput to numpy array')
            return None
        
        if newField.ndim is not 2: # reads number of dimensions of numpy array
            logging.warning('listInput dimension has wrong shape. It should be a two dimensional List.')
            return None

        newField = np.where(newField == 0, 0, 1)
        return newField

