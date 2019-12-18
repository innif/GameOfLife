import numpy as np
import logging

class Template():
    def __init__(self, name, data = None, shape = (1,1)):
        self.shape = shape
        self.name = name
        self._pointlist = []

        if data is not None:
            self.set_field(data)

    def __str__(self):
        return str(self.get_field())
    
    def get_field(self):
        out = np.zeros(self.shape)
        for p in self._pointlist:
            out[p] = 1
        return out

    def set_field(self, data):
        ''' data - anything twodimensional that can be converted to a numpy array '''
        data = np.array(data)
        if(data.ndim is not 2):
            raise ValueError('The input has more or less than two dimensions')

        if(data.shape):
            logging.info('wrong shape of input data, changing template shape')
            self.shape = data.shape
        
        px, py = np.where(data == 1)

        l = zip(px.astype(int), py.astype(int))
        l = list(l)
        l = [(i.item(), j.item()) for i,j in l]

        self._pointlist = l