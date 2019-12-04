#TODO figure selection
#TODO Performance
#TODO define alowed placing Areas
#TODO coding style
#TODO add docstrings

import time

from field import Field
from display import Display
import figures

size = 10, 10

f = Field(size=size, initValue=0)

#f.placeFigure(figures.pentadecathlon, (10,10))
f.fillRandom(seed=0)
f.setField('Hallo')

d = Display(f.getSize(), 800)
d.setField(f)
f.loadFromFile('field.f')

while(True):
    d.loadFigure(figures.gliderHorizontal)
    d.drawField(f)
    d.mainloop()
    f.update()
