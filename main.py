#TODO figure selection
#TODO Performance
#TODO define alowed placing Areas
#TODO coding style
#TODO add docstrings

import time

from field import Field
from display import Display
import figures

size = 300,300

f = Field(size=size, initValue=0)

#f.placeFigure(figures.pentadecathlon, (10,10))
#f.fillRandom(seed=0)

d = Display(f.getSize(), 1000)
d.setField(f)

while(True):
    d.loadFigure(figures.gliderDiagonalNE)
    d.drawField(f)
    d.mainloop()
    start_time=time.time()
    f.update()
    stop_time=time.time()
    print(stop_time-start_time)
