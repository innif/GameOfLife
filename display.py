import tkinter as tk
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

    def drawPixel(self, pos):
        x, y = pos
        xPixel, yPixel = int(x*self.blockSize), int(y*self.blockSize)
        pygame.draw.rect(self.screen, (0,0,255), (xPixel, yPixel, self.blockSizePixel, self.blockSizePixel))

    def drawField(self, field):
        self.screen.fill((200,200,200))
        w, h = self.fieldSize
        for y in range(0, h):
            for x in range(0, w):
                pos = x,y
                if field.getPixel(pos) == 1:
                    self.drawPixel(pos)
        
    def mainloop(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()