import random
import numpy as np
from scipy.signal import convolve2d
import logging

class Field():
    def __init__(self, size = (0,0), initValue = 0, copy_field=None):
        if copy_field is not None:
            self.size = copy_field.size
            self.field = copy_field.field.copy()
        else:
            self.size = size
            self.field = self.generate_field(initValue)

    def fill_random(self, seed = None):
        if seed is not None:
            np.random.seed(seed)
        w, h = self.size
        r = np.random.rand(h, w)
        self.field = np.where(r > 0.5, 1, 0).astype(np.int8)

    def fill_field(self, value):
        self.field = self.generate_field(value)

    def set_field(self, field):
        ''' sets the field to the given value. 0 means dead, everything else means alive (should be a byte-number)
            
            field -> two dimensional list
        '''
        newField = self.to_field_array(field)
        if newField is None:
            logging.warning('set_field() failed')
            return
        self.size = newField.shape # update field size
        self.size = self.size[1], self.size[0]
        self.field = newField

    def place_figure(self, figure, offset = (0,0)):
        ''' places a figure at the given offset
        
        figure -> anything that can be converted to a numpy array '''

        figure = self.to_field_array(figure)
        if figure is None:
            logging.warning('place_figure() failed')
            return
        
        self.place_numpy_array(figure, offset)

    def place_template(self, template, offset = (0,0)):
        ''' places an object of the template class at the given offset
        
        figure -> anything that can be converted to a numpy array '''
        self.place_pointlist(template._pointlist, offset=offset)

    def place_pointlist(self, pointlist, offset=(0,0)):
        xOff, yOff = offset
        w, h = self.size
        for p in pointlist:
            x, y = p
            place = (y+yOff)%h, (x+xOff)%w
            self.field[place] = 1


    def get_pixel(self, pos):
        x, y = pos
        # print(str(pos)+' - '+str(self.field[x ,y]))
        return self.field[y, x]

    def update(self):
        neighboursCount = self.neighbours_matrix()
        survivorsA = neighboursCount >= 2
        survivorsB = neighboursCount <= 3
        self.field = self.field*survivorsA*survivorsB
        self.field = np.where(neighboursCount == 3, 1, self.field)

    def load_from_file(self, path):
        f = open(path, 'r')
        lines = f.readlines()
        w = len(lines[0])-1 # laenge des ersten Strings -1, da jede Zeile auf \n endet

        field = []
        for l in lines:
            l = [char for char in l[0:w]]
            field.append(l)

        field = np.array(field)
        field = np.where(field == '#', 1, 0)
        self.set_field(field)

    def print(self):
        print('Field: ')
        w, h = self.size
        for y in range(h):
            for x in range(w):
                pos = x, y
                print('#' if self.get_pixel(pos)>0 else ' ', end='')
            print('')

    def place_numpy_array(self, array, offset):
        hFig, wFig = array.shape[:2] 
        x1, y1 = offset
        w, h = self.size

        for x in range(wFig):
            for y in range(hFig):
                self.field[(y1+y)%h, (x1+x)%w] += array[y, x]
            
    def neighbours_matrix(self):
        field = self.field
        kernel = np.array(
            [
                [1,1,1],
                [1,0,1],
                [1,1,1],
            ]
        )
        neighboursCount = convolve2d(field, kernel, mode='same', boundary='wrap')
        return neighboursCount

    def set_pixel(self, pos, state):
        x, y = pos
        self.field[y, x] = state

    def generate_field(self, value):
        w, h = self.size
        return np.full((h, w), value).astype(np.int8)

    def to_field_array(self, listInput):
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

