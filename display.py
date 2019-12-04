import pygame
import sys
import numpy as np
import colorsets
import logging

class Display():
    def __init__(self, fieldSize, windowHeight = 400):
        pygame.init()
        self.fieldSize = w, h = fieldSize 
        self.blockSize = windowHeight/h
        self.windowHeight = windowHeight
        self.blockSizePixel = round(self.blockSize)
        self.screenSize = int(self.blockSize*w), int(self.blockSize*h)
        self.screen = pygame.display.set_mode(self.screenSize)
        self.loadedFigure = None
        self.field = None # must be set for placing Figures
        self.loadedFigureShape = (0,0)
        self.colors = colorsets.blue
    def loadFigure(self, figure):
        self.loadedFigure = figure
        self.loadedFigureShape = len(figure[0]), len(figure)

    def setField(self, field):
        self.field = field

    def setColors(self, colors):
        self.colors = colors

    def drawPixel(self, pos, color = (0,223,252)):
        x, y = pos
        xPixel, yPixel = int(x*self.blockSize), int(y*self.blockSize)
        pygame.draw.rect(self.screen, color, (xPixel, yPixel, self.blockSizePixel, self.blockSizePixel))

    def drawGrid(self, color):
        blockSizeX = self.screenSize[0]/self.fieldSize[0]
        blockSizeY = self.screenSize[1]/self.fieldSize[1]

        if blockSizeX < 10 or blockSizeY < 10:
            return

        for x in range(1,self.fieldSize[0]):
            pygame.draw.line(self.screen, color, (x*blockSizeX, 0), (x*blockSizeX, self.screenSize[1]))
        
        for y in range(1,self.fieldSize[1]):
            pygame.draw.line(self.screen, color, (0, y*blockSizeY), (self.screenSize[0], y*blockSizeY))

    def drawField(self, field):
        self.screen.fill(self.colors.get('background'))
        field = field.getArray()
        field = np.swapaxes(field,0,1)

        pixels = np.full((field.shape[0], field.shape[1], 3), 0)
        pixels[:,:,0] = np.where(field, self.colors.get('pixel')[0], self.colors.get('background')[0])
        pixels[:,:,1] = np.where(field, self.colors.get('pixel')[1], self.colors.get('background')[1])
        pixels[:,:,2] = np.where(field, self.colors.get('pixel')[2], self.colors.get('background')[2])

        if self.loadedFigure is not None:
            pos = pygame.mouse.get_pos()

            wFig, hFig = self.loadedFigureShape
            drawX, drawY = int(pos[0]/self.blockSize- wFig/2), int(pos[1]/self.blockSize - hFig/2)
            w, h = self.fieldSize
            
            for y, row in enumerate(self.loadedFigure):
                for x, pixel in enumerate(row):
                    if(pixel == 1):
                        try:
                            pixels[(drawX+x)%w, (drawY+y)%h, :] = self.colors.get('preview')
                        except:
                            pass

        s = pygame.pixelcopy.make_surface(pixels)
        s = pygame.transform.scale(s, self.screenSize)

        self.screen.blit(s, (0,0))

        if self.colors.get('gridVisible'):
            self.drawGrid(self.colors.get('grid'))

        
    def mainloop(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
                ev = pygame.event.get()
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                if self.loadedFigure is not None and self.field is not None:
                    pos = pygame.mouse.get_pos()
                    w, h = self.loadedFigureShape
                    drawPos = round(pos[0]/self.blockSize - w/2), round(pos[1]/self.blockSize - h/2)
                    self.field.placeFigure(self.loadedFigure, drawPos)
                    self.loadedFigure = None

        pygame.display.update()