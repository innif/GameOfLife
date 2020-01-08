import pyglet
import numpy as np
from pyglet.gl import *

import colorsets
import figures
from screen import Screen
from field import Field
from template import Template

# has to be executed as __main__
class GUI():
    def __init__(self, field, height = 800, color = colorsets.blue):
        self.field = field
        self.color = color

        h = height
        w = h*16//9
        self.window = pyglet.window.Window(w, h)
        glEnable(GL_TEXTURE_2D)                                                                                                                           

        self.screen = Screen(self.field.size_)
        self.screen.setColors(self.color)

        self.window.set_caption("Cellular Automaton")
        self.label = pyglet.text.Label('Hello, world!',
                                        font_name='Arial',
                                        font_size=36,
                                        x=self.window.width // 2,
                                        y=self.window.height // 2,
                                        anchor_x='center',
                                        anchor_y='center')
        
        @self.window.event
        def on_draw():
            self.window.clear()
            self.label.draw()

            self.screen.drawField(self.field)

            text = self._array_to_texture(self.screen.rgb_matrix, (self.window.width*0.9,self.window.height*0.9))
            text.blit(int(self.window.width * 0.05), 0, 0)

    def run(self):
        pyglet.app.run()

    def _array_to_texture(self, array, size):
        h, w, _ = array.shape
        array = np.flip(array,0)
        img = pyglet.image.ImageData(width=w, height=h, format="RGB", data=bytes(array))
        text = img.get_texture()   
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)                                                                                                                               
        text.width = int(size[0])                                                                                                                                                             
        text.height = int(size[1])     
        return text


t = Template('GLIDER', figures.gliderDiagonalNE)
f = Field((160,90))
f.fillRandom()
f.placeTemplate(t,(2,2))
def update(dt):
    f.update()
g = GUI(f)
pyglet.clock.schedule_interval(update, 1.0 / 100.0)
g.run()

#-------
#-------
#--#----
#--#-# --
#--##---