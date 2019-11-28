import time

from field import Field
from display import Display

gliderDiagonal = [
    [0,1,0],
    [0,0,1],
    [1,1,1],
]

gliderHorizontal = [
    [0,1,1,1,1,1,1],
    [1,0,0,0,0,0,1],
    [0,0,0,0,0,0,1],
    [1,0,0,0,0,1,0],
    [0,0,1,1,0,0,0]
]

pentadecathlon = [
    [1,1,1],
    [1,0,1],
    [1,1,1],
    [1,1,1],
    [1,1,1],
    [1,1,1],
    [1,0,1],
    [1,1,1],
]

stick = [
    [1, 1, 0, 0, 0, 0, 0,],
    [1, 0, 1, 0, 0, 0, 0,],
    [0, 1, 0, 1, 0, 0, 0,],
    [0, 0, 1, 0, 1, 0, 0,],
    [0, 0, 0, 1, 0, 1, 0,],
    [0, 0, 0, 0, 1, 0, 1,],
    [0, 0, 0, 0, 0, 1, 1,]
]

size = 50,50

f = Field(size=size, initValue=0)
#f.fillRandom()
#f.setField(array)
# for i in range(10):
#     for j in range(1, 10):
#         f.placeFigure(gliderHorizontal, (i*10,j*10))
#f.placeFigure(pentadecathlon, (150,150))
#f.placeFigure(stick, (150,100))

#f.fillRandom(seed=0)
d = Display(f.getSize(), 1000)
d.loadFigure(gliderHorizontal)
d.setField(f)

while(True):
    d.loadFigure(gliderHorizontal)
    d.drawField(f)
    d.mainloop()
    #time.sleep(1)
    f.update()
