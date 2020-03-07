import pygame
import math as mth
from wall import *
from checkpiont import *

pygame.init()

WIDTH = 1300
HEIGHT = 820

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT)) # to make full screen do : , pygame.FULLSCREEN
pygame.display.set_caption("make track")
pygame.display.update()

walls = []
checkpionts = []
mode = 0
begin_pos = []
end_pos = []
snap_dist = 10
second_mouse_press_first = True
state = 0
checkpiont_score = 0

fontL = pygame.font.SysFont(None, 100)
fontS = pygame.font.SysFont(None, 30)


def message_toscreen(msg, color, x, y, size):
    if (size == "l"):
        screenText = fontL.render(msg, True, color)
        gameDisplay.blit(screenText, [x, y])
    if (size == "s"):
        screenText = fontS.render(msg, True, color)
        gameDisplay.blit(screenText, [x, y])


def draw_line(pos1, pos2, color):
    pygame.draw.line(gameDisplay, color, pos1, pos2)

def dist(x1, x2, y1, y2):
    return mth.sqrt(mth.pow(x1-x2, 2) + mth.pow(y1-y2, 2))

gameExit = False

while not gameExit:
    if state == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    state = 1

        # updates
        if pygame.mouse.get_pressed()[2]:
            if second_mouse_press_first:
                mode += 1
                if mode > 2:
                    mode = 0
                second_mouse_press_first = False
        elif not pygame.mouse.get_pressed()[2]:
            second_mouse_press_first = True

        if pygame.mouse.get_pressed()[0]:
            if not mouse_first_pressed:
                begin_pos = pygame.mouse.get_pos()
            mouse_first_pressed = True
        elif not pygame.mouse.get_pressed()[0]:
            mouse_first_pressed = False
            if not begin_pos == []:
                end_pos = pygame.mouse.get_pos()
                for w in walls:
                    if dist(begin_pos[0], w.start_pos[0], begin_pos[1], w.start_pos[1]) < snap_dist:
                        begin_pos = w.start_pos
                    elif dist(begin_pos[0], w.end_pos[0], begin_pos[1], w.end_pos[1]) < snap_dist:
                        begin_pos = w.end_pos
                    elif dist(end_pos[0], w.end_pos[0], end_pos[1], w.end_pos[1]) < snap_dist:
                        end_pos = w.end_pos
                    elif dist(end_pos[0], w.start_pos[0], end_pos[1], w.start_pos[1]) < snap_dist:
                        end_pos = w.start_pos
                for ch in checkpionts:
                    if dist(begin_pos[0], ch.start_pos[0], begin_pos[1], ch.start_pos[1]) < snap_dist:
                        begin_pos = ch.start_pos
                    elif dist(begin_pos[0], ch.end_pos[0], begin_pos[1], ch.end_pos[1]) < snap_dist:
                        begin_pos = ch.end_pos
                    elif dist(end_pos[0], ch.end_pos[0], end_pos[1], ch.end_pos[1]) < snap_dist:
                        end_pos = ch.end_pos
                    elif dist(end_pos[0], ch.start_pos[0], end_pos[1], ch.start_pos[1]) < snap_dist:
                        end_pos = ch.start_pos

                if mode == 0:
                    walls.append(Wall(begin_pos, end_pos))
                elif mode == 1:
                    checkpionts.append(Checkpoint(begin_pos, end_pos, checkpiont_score, False))
                    checkpiont_score += 1
                elif mode == 2:
                    checkpionts.append(Checkpoint(begin_pos, end_pos, checkpiont_score, True))
                    checkpiont_score += 1
                begin_pos = []
    
        # draw
        gameDisplay.fill(0)

        if pygame.mouse.get_pressed()[0]:
            draw_line(begin_pos, pygame.mouse.get_pos(), (255, 255, 255))
        
        message_toscreen("mode: " + str(mode), (255, 255, 255), 10, 30, "s")

        for w in walls:
            draw_line(w.start_pos, w.end_pos, w.color)
            pygame.draw.circle(gameDisplay, (255, 0, 0), w.start_pos, snap_dist)
            pygame.draw.circle(gameDisplay, (255, 0, 0), w.end_pos, snap_dist)
        for ch in checkpionts:
            draw_line(ch.start_pos, ch.end_pos, ch.color)
            pygame.draw.circle(gameDisplay, (255, 0, 0), ch.start_pos, snap_dist)
            pygame.draw.circle(gameDisplay, (255, 0, 0), ch.end_pos, snap_dist)

        pygame.draw.circle(gameDisplay, (255, 0, 0), [int(WIDTH/2), int(HEIGHT/2+100)], 20)

        pygame.display.update()


    elif state == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
        

        
        # draw
        gameDisplay.fill(0)
        message_toscreen("go to terminal to give name of track", (255, 255, 255), 10, 30, "s")
        pygame.display.update()
        name_inp = str(input("name of track: "))
        f = open("tracks/" + name_inp + ".track", "w")
        for w in walls:
            f.write(str(w.start_pos[0]) + ", " + str(HEIGHT - w.start_pos[1]) + ", " + str(w.end_pos[0]) + ", " + str(HEIGHT - w.end_pos[1]) + "\n")
        f.write("ch\n")
        for ch in checkpionts:
           f.write(str(ch.start_pos[0]) + ", " + str(HEIGHT - ch.start_pos[1]) + ", " + str(ch.end_pos[0]) + ", " + str(HEIGHT - ch.end_pos[1]) + ", " + str(ch.score) + ", " + str(ch.is_finish) + "\n") 
        
        break

pygame.quit()
quit()