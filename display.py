import tkinter as tk

class Display():
    def __init__(self, fieldSize, windowHeight = 400):
        self.fieldSize = w, h = fieldSize 
        self.windowHeight = windowHeight
        self.blockSize = windowHeight/h
        self.window = tk.Tk('Conways Game of Life')
        self.canvas = tk.Canvas(master=self.window, width=self.blockSize*w, height=self.blockSize*h)
        self.canvas.pack()

    def drawPixel(self, pos):
        x, y = pos
        xPixel, yPixel = int(x*self.blockSize), int(y*self.blockSize)
        self.canvas.create_rectangle(xPixel, yPixel, xPixel+self.blockSize, yPixel+self.blockSize, fill="blue", outline="blue", tags='pixel')

    def drawField(self, field):
        w, h = self.fieldSize
        try:
            self.canvas.delete('all')
        except:
            pass
        
        for y in range(0, h):
            for x in range(0, w):
                pos = x,y
                if field.getPixel(pos) == 1:
                    self.drawPixel(pos)

    def mainloop(self):
        self.window.update_idletasks()
        self.window.update()
