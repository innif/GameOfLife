import random
import numpy as np

class Field():
    def __init__(self, size, initValue = 0):
        self.size = w, h = size
        self.field = self._generateField(initValue)
        self.numberOfNeighbours = np.zeros(self.size, np.int8)
        self.newNumberOfNeighbours = np.zeros(self.size, np.int8)
        self._initializeCountNeighbours()

    def getSize(self):
        return self.size

    def fillRandom(self, seed = None):
        if seed is not None:
            random.seed(seed)
        w, h = self.size
        r = np.random.rand(h, w)
        self.field = np.where(r > 0.5, 1, 0).astype(np.int8)
        self._initializeCountNeighbours()

    def fillField(self, value):
        self.field = self._generateField(value)
        self._initializeCountNeighbours()

    def setField(self, field):
        #TODO Fehlererkennung
        self.field = np.array(field).astype(np.int8)
        self._initializeCountNeighbours()

    def placeFigure(self, figure, offset = (0,0)):
        #TODO Fehlererkennung
        h, w = np.array(figure).shape
        x1, y1 = offset
        x2, y2 = x1+w, y1+h
        self.field[y1:y2, x1:x2] = figure
        self._initializeCountNeighbours()

    def getField(self):
        return self.field

    def getPixel(self, pos):
        x, y = pos
        # print(str(pos)+' - '+str(self.field[x ,y]))
        return self.field[y, x]

    def update(self):
        self.newNumberOfNeighbours = np.copy(self.numberOfNeighbours)
        w, h = self.size
        #newField = [[self._newState((x,y)) for x in range(w)] for y in range(h)]
        newField = np.zeros((h, w), np.int8)
        for y in range(h):
            for x in range(w):
                newField[y, x] = self._newState((x, y))
        self.field = newField
        self.numberOfNeighbours = self.newNumberOfNeighbours

    def loadFromFile(self, path):
        #TODO
        self._initializeCountNeighbours()
        pass

    def print(self):
        print('Field: ')
        w, h = self.size
        for y in range(h):
            for x in range(w):
                pos = x, y
                print('#' if self.getPixel(pos)>0 else ' ', end='')
            print('')

    def _setPixel(self, pos, state):
        x, y = pos
        self.field[y, x] = state

    def _generateField(self, value):
        w, h = self.size
        field = np.full((h, w), value).astype(np.int8)
        return field

    def _newState(self, pos):
        x, y = pos

        neighbours = self.numberOfNeighbours[y, x]

        if neighbours == 0:
            return 0

        state = self.getPixel(pos)
        newState = state

        if(neighbours < 3):
            newState = 0 # stirbt an Einsamkeit

        if(state == 0 and neighbours == 3):
            newState = 1 # wird geboren

        if(state == 1 and neighbours > 4):
            newState = 0 # stirbt wegen Überbevölekrung

        self._updateNeighbourCount(pos, newState-state)

        return newState

    def _updateNeighbourCount(self, pos, diff):
        if diff == 0:
            return
        x, y = pos
        w, h = self.size
        x1, x2 = max(x-1, 0), min(x+2, w)
        y1, y2 = max(y-1, 0), min(y+2, h)
        self.newNumberOfNeighbours[y1:y2, x1:x2] += diff

    def _countNeighbours(self, pos, throughWall = False):
        ''' counts the number of not zero values in the neighbourhood of pos, including pos itself'''
        w, h = self.size
        x, y = pos

        if(throughWall):
            x1, x2 = x-1 if x-1>0 else x-1+w, (x+1 % w)+1
            y1, y2 = y-1 if y-1>0 else y-1+h, (y+1 % h)+1
            #TODO Wenn über Kante hinweg reinfolge falsch
        else:
            x1, x2 = max(x-1, 0), min(x+2, w)
            y1, y2 = max(y-1, 0), min(y+2, h)

        subField = self.field[y1:y2, x1:x2]
        neighbours = np.count_nonzero(subField)
        return neighbours

    def _initializeCountNeighbours(self):
        #TODO Optimize
        w, h = self.size
        for y in range(h):
            for x in range(w):
                pos = x,y
                self.numberOfNeighbours[y, x] = self._countNeighbours(pos)
