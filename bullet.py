from ray import *
from network import *
import math as mth
import random as r
import pyglet

class Bullet:

    def __init__(self, _pos, _rot, _owner):
        # variables for bullet
            # game
        self.pos = _pos
        self.rot = _rot
        self.owner = _owner
        self.vel = [1, 0]
        self.accel = [0, 0]
        self.dead = False
        self.size = 5
        self.speed = 300
        self.rot_speed = 125
        self.boundries = []
            # draw
        self.color = (255,0,0,255)
        self.img = pyglet.resource.image("hot_dog.png")
        self.img.width = self.size * 2
        self.img.height = self.size
        self.img.anchor_x = self.img.width/2
        self.img.anchor_y = self.img.height/2
        self.sprite = pyglet.sprite.Sprite(self.img)
        # add img boundries to list
        self.boundries.append([self.pos[0], self.pos[1], self.pos[0], self.pos[1], self.img.width/2, self.img.height/2, -self.img.width/2, -self.img.height/2])
        self.boundries.append([self.pos[0], self.pos[1], self.pos[0], self.pos[1], -self.img.width/2, self.img.height/2, self.img.width/2, -self.img.height/2])
        #create rays
    

    def move(self, delta_time):
        temp_rot = self.rot
        temp_pos = self.pos
        self.sprite.rotation = -self.rot
        self.accel[0] = mth.cos(mth.radians(self.rot))
        self.accel[1] = mth.sin(mth.radians(self.rot))
        self.vel[0] = self.accel[0]
        self.vel[1] = self.accel[1]
        self.pos[0] += self.speed * delta_time * self.vel[0]
        self.pos[1] += self.speed * delta_time * self.vel[1]
        self.sprite.x = self.pos[0]
        self.sprite.y = self.pos[1]
        self.move_boundries(temp_rot, temp_pos)

    
    def move_boundries(self, rot, old_pos):
        amount_of_rot = self.rot
        for line in self.boundries:
            line[0] = self.pos[0] + (line[4] * mth.cos(mth.radians(amount_of_rot))) - (line[5] * mth.sin(mth.radians(amount_of_rot)))
            line[1] = self.pos[1] + (line[4] * mth.sin(mth.radians(amount_of_rot))) + (line[5] * mth.cos(mth.radians(amount_of_rot)))
            line[2] = self.pos[0] + (line[6] * mth.cos(mth.radians(amount_of_rot))) - (line[7] * mth.sin(mth.radians(amount_of_rot)))
            line[3] = self.pos[1] + (line[6] * mth.sin(mth.radians(amount_of_rot))) + (line[7] * mth.cos(mth.radians(amount_of_rot)))

    
    def check_for_hit(self, walls):
        for line in self.boundries:
            for wall in walls:
                x1 = wall.start_pos[0]
                y1 = wall.start_pos[1]
                x2 = wall.end_pos[0]
                y2 = wall.end_pos[1]

                x3 = line[0]
                y3 = line[1]
                x4 = line[2]
                y4 = line[3]
                if self.lineline_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
                    self.dead = True

    
    def lineline_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        if ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)) == 0:
            return False
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
            return True
        return False


    def out_off_bounds(self, xmax, ymax):
        if self.pos[0] < 0 or self.pos[0] > xmax or self.pos[1] < 0 or self.pos[1] > ymax:
            self.dead = True