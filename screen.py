import pygame
import sys
import numpy as np
import colorsets
import logging

class Screen():
    def __init__(self, fieldSize):
        self.fieldSize = w, h = fieldSize 
        self.pixels = np.zeros(fieldSize)
        self.colors = colorsets.blue

    def getScreen(self):
        s = pygame.pixelcopy.make_surface(self.pixels)
        return s

    def setColors(self, colors):
        self.colors = colors

    def previewTemplate(self, pos, template):
        if template is None:
            return

        pointlist = template.get_pointlist()

        drawX, drawY = pos
        w, h = self.fieldSize

        for p in pointlist:
            x, y = p
            self.pixels[(drawX+x)%w, (drawY+y)%h, :] = self.colors.get('preview')


    def drawField(self, field):
        # background = np.ones((field.shape[0], field.shape[1], 3), 0)
        # background *= np.array(self.colors.get('background'))

        # foreground = np.ones((field.shape[0], field.shape[1], 3), 0)
        # foreground *= np.array(self.colors.get('pixel'))

        field = field.getArray()
        field = np.swapaxes(field,0,1)

        bColor = np.array(self.colors.get('background'))
        fColor = np.array(self.colors.get('pixel'))

        pixels = np.zeros((*self.fieldSize, 3), np.uint8)

        for i in range(3):
            pixels[:, :, i] = np.where(field, fColor[i], bColor[i])

        self.pixels = pixels