import math as mth

class Ray:

    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir
        self.vect = [mth.cos(self.dir), mth.sin(self.dir)]
    

    def blit(self):
        pygame.draw.line(
            gameDisplay,
            light_grey,
            [int(self.pos[0] + translationX),int(self.pos[1] + translationY)],
            [int(self.pos[0] + translationX + self.vect[0] * 20), int(self.pos[1] + translationY + self.vect[1] * 20)]
        )


    def rotate_ray(self, add):
        self.dir += add
        self.vect = [mth.cos(self.dir), mth.sin(self.dir)]


    def cast(self, wall):
        x1 = wall.start_pos[0]
        y1 = wall.start_pos[1]
        x2 = wall.end_pos[0]
        y2 = wall.end_pos[1]

        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.vect[0]
        y4 = self.pos[1] + self.vect[1]

        den = (x1 - x2) * (y3 - y4) - (x3 - x4) * (y1 - y2)

        if den == 0:
            self.cast_hit = False
            return False
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            ptx = x1 + t * (x2 - x1)
            pty = y1 + t * (y2 - y1)
            pt = [ptx, pty]
            self.cast_hit_point = pt
            self.cast_hit = True
            return pt
        else:
            self.cast_hit = False
            return False