import pygame

class SelectionField():
    def __init__(self, size): 
        self.size = w, h = size # w,h
        self.surface = pygame.Surface(size)
        self.template_list = []
        self.template_size = w # all previews are in square-shape
        self.template_distance = 20
        self._tile_offset = 0
        self.total_height = 0
        self.hover_area = 100

    def add_template(self, template):
        self.template_list.append(template)
        self.total_height += (self.template_size+self.template_distance)

    def scroll_up(self, dist = 1):
        self._tile_offset += dist
        self._tile_offset = min(self._tile_offset, self.total_height)

    def scroll_down(self, dist = 1):
        self._tile_offset -= dist
        self._tile_offset = max(self._tile_offset, -self.total_height)

    def hover_update(self, mousepos):
        if mousepos[y] < self.hover_area:
            self.scroll_up()

    def update_surface(self, bgColor):
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bgColor)
        for y, t in enumerate(self.template_list):
            y = y * (self.template_size+self.template_distance)
            y += self._tile_offset

            if y > self.size[1]:
                continue
            surf = t.surface
            surf = pygame.transform.scale(surf, (self.template_size, self.template_size))
            self.surface.blit(surf, (0,y))

        

    