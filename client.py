#import argparse


import socket

server_ip = 'localhost'
port = 1111

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, port))

from field import Field
from display import Display
import figures

size = 50,50

f = Field(size=size, initValue=0)

#f.placeFigure(figures.pentadecathlon, (10,10))
#f.fillRandom(seed=0)

d = Display(f.getSize(), 1000)
d.setField(f)

while(True):
    d.loadFigure(figures.gliderDiagonalNE)
    d.drawField(f)
    d.mainloop()
    f.update()


