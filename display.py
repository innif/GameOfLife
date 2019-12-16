import pygame
import sys

class Display():
    def __init__(self, fieldSize, windowHeight = 400):
        pygame.init()
        self.fieldSize = w, h = fieldSize 
        self.windowHeight = windowHeight
        self.blockSize = windowHeight/h
        self.blockSizePixel = round(self.blockSize)
        self.screen = pygame.display.set_mode((int(self.blockSize*w), int(self.blockSize*h)))
        self.loadedFigure = None
        self.field = None # must be set for placing Figures
        self.loadedFigureShape = (0,0)

    def loadFigure(self, figure):
        self.loadedFigure = figure
        self.loadedFigureShape = len(figure[0]), len(figure)

    def setField(self, field):
        self.field = field

    def setColors(self, colors):
        pass
        #TODO pass color as Lexika

    def drawPixel(self, pos, color = (0,223,252)):
        x, y = pos
        xPixel, yPixel = int(x*self.blockSize), int(y*self.blockSize)
        pygame.draw.rect(self.screen, color, (xPixel, yPixel, self.blockSizePixel, self.blockSizePixel))

    def drawField(self, field):
        self.screen.fill((52,56,56))
        w, h = self.fieldSize
        for y in range(0, h):
            for x in range(0, w):
                pos = x,y
                if field.getPixel(pos) == 1:
                    self.drawPixel(pos)
        
    def mainloop(self):
        if self.loadedFigure is not None:
            self.previewFigure(self.loadedFigure)

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

    def previewFigure(self, figure):
        pos = pygame.mouse.get_pos()

        w, h = self.loadedFigureShape
        drawX, drawY = round(pos[0]/self.blockSize- w/2), round(pos[1]/self.blockSize - h/2)
        
        for y, row in enumerate(figure):
            for x, pixel in enumerate(row):
                if(pixel == 1):
                    self.drawPixel((drawX+x, drawY+y), color = (0,95,107))