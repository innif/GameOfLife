import pygame
import sys
import numpy as np

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

    def loadFigure(self, figure):
        self.loadedFigure = figure
        self.loadedFigureShape = len(figure[0]), len(figure)

    def setField(self, field):
        self.field = field

    def setColors(sekf, colors):
        pass
        #TODO pass color as Lexika

    def drawPixel(self, pos, color = (0,223,252)):
        x, y = pos
        xPixel, yPixel = int(x*self.blockSize), int(y*self.blockSize)
        pygame.draw.rect(self.screen, color, (xPixel, yPixel, self.blockSizePixel, self.blockSizePixel))

    def drawField(self, field):
        self.screen.fill((52,56,56))
        field = field.getArray()
        field = np.swapaxes(field,0,1)

        pixels = np.full((field.shape[0], field.shape[1], 3), 0)
        pixels[:,:,0] = np.where(field, 0, 52)
        pixels[:,:,1] = np.where(field, 223, 56)
        pixels[:,:,2] = np.where(field, 252, 56)

        if self.loadedFigure is not None:
            pos = pygame.mouse.get_pos()

            w, h = self.loadedFigureShape
            drawX, drawY = int(pos[0]/self.blockSize- w/2), int(pos[1]/self.blockSize - h/2)
            
            for y, row in enumerate(self.loadedFigure):
                for x, pixel in enumerate(row):
                    if(pixel == 1):
                        try:
                            pixels[drawX+x, drawY+y,0] = 0
                            pixels[drawX+x, drawY+y,1] = 95
                            pixels[drawX+x, drawY+y,2] = 107
                        except:
                            pass

        s = pygame.pixelcopy.make_surface(pixels)
        s = pygame.transform.scale(s, self.screenSize)

        self.screen.blit(s, (0,0))
        
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