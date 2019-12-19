import pygame
import sys
import numpy as np
import logging

import colorsets
import figures

from selectionfield import SelectionField
from screen import Screen
from template import Template

class Display():
    def __init__(self, fieldSize, screenSize = (400, 400), mainFieldHeight = 380):
        #TODO NUR height übergeben
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption("Conway's Game of Life")
        self.mainField = Screen(fieldSize)

        self.fieldSize = fW, fH = fieldSize
        self.screenSize = w, h =  screenSize

        self.field = None
        self.loadedTemplate = None

        mainScreenSize = mW, mH = int(mainFieldHeight*fW/fH), mainFieldHeight
        margin = int((h-mH)/2)

        self.mainScreenRect = (w-mW-margin, margin, mW, mH)
        
        self.selectionField = SelectionField((100, mainFieldHeight))
        self.selectionFieldRect = (margin, margin, *self.selectionField.size)

        self.selectionField.add_template(Template('Test', figures.pentadecathlon))
        self.selectionField.add_template(Template('Test', figures.gliderDiagonalSE))
        self.selectionField.add_template(Template('Test', figures.stick))

    def loadTemplate(self, template):
        self.loadedTemplate = template

    def setField(self, field):
        self.field = field

    def setColors(self, colors):
        self.colors = colors
        self.mainField.setColors(colors) #TODO

    def drawField(self, field):
        self.screen.fill(self.colors.get('main-background'))

        self.mainField.drawField(field)
        self.selectionField.update_surface(self.colors.get('main-background'))

        mPos = self.getMousePixelPos()
        if(mPos is not None and self.loadedTemplate is not None):
            self.mainField.previewTemplate(self.getMousePixelPos(), self.loadedTemplate)

        pos, size = self.mainScreenRect[0:2], self.mainScreenRect[2:4]

        surf = self.mainField.getScreen()
        surf = pygame.transform.scale(surf, size)

        self.screen.blit(surf, pos)

        pos, size = self.selectionFieldRect[0:2], self.selectionFieldRect[2:4]

        surf = self.selectionField.surface
        surf = pygame.transform.scale(surf, size)

        self.screen.blit(surf, pos)
        
    def mainloop(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
                ev = pygame.event.get()
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONDOWN:#pygame.MOUSEBUTTONUP:
                if self.loadedTemplate is not None and self.field is not None:
                    pos = self.getMousePixelPos()
                    if pos is None:
                        return
                    self.field.placeTemplate(self.loadedTemplate, pos)
                    self.loadedTemplate = None

        pygame.display.update()

    def getMousePixelPos(self):
        xScreen, yScreen = self.mainScreenRect[0:2]
        wScreen, hScreen = self.mainScreenRect[2:4]
        w, h = self.fieldSize

        x, y = pygame.mouse.get_pos()
        x, y = x-xScreen, y-yScreen
        x, y = x/wScreen, y/hScreen
        x, y = x*w, y*h

        if x < 0 or y < 0 or x >= w or y >= h:
            return None 

        return int(x), int(y)