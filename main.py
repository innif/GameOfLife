#TODO figure selection
#TODO Performance
#TODO define alowed placing Areas
#TODO coding style
#TODO add docstrings

import time

from field import Field
from display import Display
import figures

size = 400, 300

f = Field(size=size, initValue=0)

#f.placeFigure(figures.pentadecathlon, (10,10))
#f.fillRandom(seed=0)

d = Display(f.getSize(), 800)
d.setField(f)

while(True):
    d.loadFigure(figures.pentadecathlon)
    d.drawField(f)
    d.mainloop()
    f.update()
