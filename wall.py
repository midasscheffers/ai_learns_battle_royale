import pygame
import pyglet
blue = (0, 0, 255, 255)


class Wall:

    def __init__(self, xy1, xy2):
        self.start_pos = xy1
        self.end_pos = xy2
        self.color = (0,0,255,255)

    def blit(self):
        # pygame.draw.line(
        #     gameDisplay,
        #     blue,
        #     [int(self.start_pos[0]), int(self.start_pos[1])],
        #     [int(self.end_pos[0]), int(self.end_pos[1])],
        #     2
        # )
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', ((self.start_pos[0]), (self.start_pos[1]), (self.end_pos[0]), (self.end_pos[1]))),
            ('c4B', blue)
        )
