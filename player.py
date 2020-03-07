from ray import *
from network import *
from bullet import *
import math as mth
import random as r
import copy
import pyglet

class Player:

    def __init__(self, _pos, _rot, _amount_of_rays, _selected):
        # variables for player
            # network
        self.net = Network([_amount_of_rays + 2, 2, 5])
        self.net_input = []
        self.amount_of_rays = _amount_of_rays
        self.score = 0
        self.fitness = 0
        self.check_piont = 1
        self.rays = []
        self.detections = []
        self.ray_pts = []
        self.ray_degrees = 120
        self.times_finished = 0
        self.raymode_angulair = False
            # game
        self.pos = _pos
        self.vel = [1, 0]
        self.accel = [0, 0]
        self.rot = _rot
        self.dead = False
        self.size = 20
        self.speed = 120
        self.rot_speed = 125
        self.boundries = []
        self.touching_finish = False
        self.fire_rate = 50
        self.time_since_last_fire = self.fire_rate
        self.dist_to_closest_enem = 99999
        self.kills = 0
            # draw
        self.color = (0,255,0,255)
        self.selected = _selected
        self.img = pyglet.resource.image("car.png")
        self.img.width = self.size * 2
        self.img.height = self.size
        self.img.anchor_x = self.img.width/2
        self.img.anchor_y = self.img.height/2
        self.sprite = pyglet.sprite.Sprite(self.img)
        # add img boundries to list
        self.boundries.append([self.pos[0], self.pos[1], self.pos[0], self.pos[1], self.img.width/2, self.img.height/2, -self.img.width/2, -self.img.height/2])
        self.boundries.append([self.pos[0], self.pos[1], self.pos[0], self.pos[1], -self.img.width/2, self.img.height/2, self.img.width/2, -self.img.height/2])
        #create rays
        if self.raymode_angulair:
            for i in range(0, _amount_of_rays):
                self.rays.append(Ray(self.pos, mth.radians(-self.ray_degrees/2 + i*(self.ray_degrees/(self.amount_of_rays-1)))))
                self.detections.append(0)
                self.ray_pts.append([0,0])
        else:
            for i in range(0, _amount_of_rays):
                self.rays.append(Ray(self.pos, mth.radians(i*(360/self.amount_of_rays))))
                self.detections.append(0)
                self.ray_pts.append([0,0])
    

    def move(self, delta_time):
        temp_rot = self.rot
        temp_pos = self.pos
        net_out = self.net.run(True)
        if net_out[1] == 0:
            self.rot += net_out[0] * self.rot_speed * delta_time
        elif net_out[1] == 1:
            self.rot -= net_out[0] * self.rot_speed * delta_time
        elif net_out[1] == 2:
            self.speed = 100
        elif net_out[1] == 3:
            self.speed = -100
        else:
            self.speed = 0
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
        for r in self.rays:
            r.pos = self.pos
            if net_out[1] == 0:
                r.rotate_ray(mth.radians(net_out[0] * self.rot_speed * delta_time))
            elif net_out[1] == 1:
                r.rotate_ray(mth.radians(net_out[0] * self.rot_speed * delta_time) * -1)
            else:
                pass
        self.score += 1
        self.time_since_last_fire += 1


    def move_boundries(self, rot, old_pos):
        amount_of_rot = self.rot
        for line in self.boundries:
            line[0] = self.pos[0] + (line[4] * mth.cos(mth.radians(amount_of_rot))) - (line[5] * mth.sin(mth.radians(amount_of_rot)))
            line[1] = self.pos[1] + (line[4] * mth.sin(mth.radians(amount_of_rot))) + (line[5] * mth.cos(mth.radians(amount_of_rot)))
            line[2] = self.pos[0] + (line[6] * mth.cos(mth.radians(amount_of_rot))) - (line[7] * mth.sin(mth.radians(amount_of_rot)))
            line[3] = self.pos[1] + (line[6] * mth.sin(mth.radians(amount_of_rot))) + (line[7] * mth.cos(mth.radians(amount_of_rot)))


    def get_dist_to_closest(self, players):
        record = 9999999999
        for p in players:
            if not p == self:
                dist = mth.pow(self.pos[0] - p.pos[0], 2) + mth.pow(self.pos[1] - p.pos[1], 2)
                if dist < record:
                    record = dist
        self.dist_to_closest_enem = record


    def check_for_hit(self, walls, checkpoints, bullets):
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
            
            for b in bullets:
                if not b.owner == self:
                    for bound in b.boundries:
                        x1 = bound[0]
                        y1 = bound[1]
                        x2 = bound[2]
                        y2 = bound[3]

                        x3 = line[0]
                        y3 = line[1]
                        x4 = line[2]
                        y4 = line[3]
                        if self.lineline_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
                            b.owner.kills += 1
                            self.dead = True

            # for check in checkpoints:
            #     x1 = check.start_pos[0]
            #     y1 = check.start_pos[1]
            #     x2 = check.end_pos[0]
            #     y2 = check.end_pos[1]

            #     x3 = line[0]
            #     y3 = line[1]
            #     x4 = line[2]
            #     y4 = line[3]
            #     if self.lineline_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
            #         if check.is_finish:
            #             if self.score >= len(checkpoints):
            #                 if not self.touching_finish:
            #                     self.times_finished += 1
            #                     self.touching_finish = True
                        
            #         else:
            #             self.touching_finish = False
            #             self.check_piont = check.score
                

    def shoot(self, bullets):
        net_out = self.net.run(True)
        
        if net_out[1] == 4:
            if self.time_since_last_fire > self.fire_rate:
                self.time_since_last_fire = 0
                pos = copy.deepcopy(self.pos)
                rot = copy.deepcopy(self.rot)
                return Bullet(pos, rot, self)
        return None

    
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



    def set_net_input(self):
        self.net_input = []
        for i in self.detections:
            self.net_input.append(i)
        self.net_input.append(self.rot)
        self.net_input.append(self.dist_to_closest_enem)
        self.net.set_input(self.net_input)
        

    def cast_rays(self, walls):
        for i in range(len(self.rays)):
            r = self.rays[i]
            closest = False
            record = 99999999999
            for w in walls:
                pt = r.cast(w)
                if not pt == False:
                    dist = mth.pow(self.pos[0]-pt[0], 2) + mth.pow(self.pos[1]-pt[1], 2)
                    if dist < record:
                        record = dist
                        closest = pt

            if not closest == False:
                if self.selected:
                    pass
                    # pygame.draw.line(
                    #     gameDisplay,
                    #     green,
                    #     [int(self.pos[0]), int(self.pos[1])],
                    #     [int(closest[0]), int(closest[1])]
                    # )
                self.detections[i] = record
                self.ray_pts[i] = closest
            else:
                self.detections[i] = 99999999999