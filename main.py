#TODO figure selection
#TODO Performance
#TODO define alowed placing Areas
#TODO coding style
#TODO add docstrings

import time

from field import Field
from display import Display
import figures
import pygame

size = 50, 30

f = Field(size=size, initValue=0)
c = pygame.time.Clock()

for x in range(0, 20):
    for y in range(0, 20):
        #f.placeFigure(figures.gliderDiagonalNE, (x*5, y*5))
        pass
#f.fillRandom(seed=0)
#f.setField('Hallo')
#f.loadFromFile('field.f')

d = Display(f.getSize(), 1000)
d.setField(f)
#f.loadFromFile('field.f')

while(True):
    d.loadFigure(figures.gliderHorizontal)
    d.drawField(f)
    d.mainloop()
    f.update()
    c.tick(100)
