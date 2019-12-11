#TODO figure selection
#TODO Performance
#TODO define alowed placing Areas
#TODO coding style
#TODO add docstrings

import time

from field import Field
from display import Display
from template import Template
import figures
import pygame
import colorsets
import logging

size = 100, 100

f = Field(size=size, initValue=0)
c = pygame.time.Clock()

t = Template('GLIDER', figures.gliderDiagonalNE)
f.placeTemplate(t, (5, 5))
# f.fillRandom(seed=0)

d = Display(f.getSize(), 1000)
d.setField(f)
d.setColors(colorsets.lightGray)
#f.loadFromFile('field.f')

while(True):
    d.loadTemplate(t)
    d.drawField(f)
    d.mainloop()
    f.update()
    c.tick(100)
