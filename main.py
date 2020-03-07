import pyglet
import matplotlib.pyplot as plt
import math as mth
from player import *
from wall import *
from checkpiont import *
from bullet import *
import copy
import random as r

# globals

WIDTH = 1300
HEIGHT = 820

gen = 0

gen_table = []
avr_fitness_table = []
avr_score_table = []
best_score_table = []
best_fitness_table = []
max_laps = 0

amount_of_rays = 4
players = []
am_of_players = 50
cycles = 1
graph_cycles = 20

checkpoints = []
walls = []
sim_speed = .02

bullets = []

track_name = "empty"
# track_name = "what_is_this"
# track_name = "round"
track_file_name = "tracks/" + track_name + ".track"


window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
pyglet.vsync = True
label = pyglet.text.Label("gen: 0, players: 100, max laps: 0", font_name="Comic Sans", font_size=25,
x=WIDTH/2, y=HEIGHT-25,
anchor_x="center", anchor_y="center"
)



# greate first players
for i in range(am_of_players):
    rot = 360/am_of_players * i
    players.append(Player([WIDTH/2 + mth.cos(mth.radians(rot)) * 200, HEIGHT/2 + mth.sin(mth.radians(rot)) * 200], rot, amount_of_rays, False))


def draw_line(xy1, xy2, color):
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
        ('v2i', (int(xy1[0]), int(xy1[1]), int(xy2[0]), int(xy2[1]))),
        ('c4B', (color) * 2)
    )


def reset_players(players):
    for p in players:
        p.pos = [WIDTH/2, HEIGHT/2-100]
        p.rot = 0
        p.dead = False


def all_dead(players):
    for p in players:
        if not p.dead:
            return False
    return True


def calc_avr_score(players):
    tot_score = 0
    for p in players:
        tot_score += p.score
    avr = tot_score/len(players)
    return avr


def calc_avr_fitness(players):
    tot_fit = 0
    for p in players:
        tot_fit += p.fitness
    avr = tot_fit/len(players)
    return avr


def find_best_score(players):
    best_score = 0
    for p in players:
        if p.score > best_score:
            best_score = p.score
    return best_score


def find_best_fitt(players):
    best_fit = 0
    best_fit_player = None
    for p in players:
        if p.fitness > best_fit:
            best_fit = p.fitness
            best_fit_player = p
    return best_fit, best_fit_player


def find_best_players(players):
    best_f = 0
    bPs = []
    for p in players:
        if p.fitness > best_f:
            bPs = []
            best_f = p.fitness
            bPs.append(p)
        elif p.fitness == best_f:
            bPs.append(p)
    if len(bPs) > 3:
        bPs = bPs[:3]
    return bPs


def str2bool(v):
    return v.lower() in ("1", "true")


def load_track_file(file_name):
    with open(file_name, "r") as f:
        rawfiledata = f.read().split("ch\n")
    wall_data = rawfiledata[0].split("\n")
    wall_data.pop()
    for item in wall_data:
        dat = item.split(", ")
        walls.append(Wall([int(dat[0]), int(dat[1])], [int(dat[2]), int(dat[3])]))
    checkpt_data = rawfiledata[1].split("\n")
    checkpt_data.pop()
    for item in checkpt_data:
        dat = item.split(", ")
        checkpoints.append(Checkpoint([int(dat[0]), int(dat[1])], [int(dat[2]), int(dat[3])], int(dat[4]), str2bool(dat[5])))


def repopulate(players):
    calculate_fitness(players)

    avr_fit = calc_avr_fitness(players)
    avr_score = calc_avr_score(players)
    best_fit, best_player = find_best_fitt(players)
    best_score = find_best_score(players)

    best_score_table.append(best_score)
    best_fitness_table.append(best_fit)
    avr_fitness_table.append(avr_fit)
    avr_score_table.append(avr_score)

    new_players = []
#kaas is lekker
    # bPs = find_best_players(players)
    # for bP in bPs:
    #     p = Player([WIDTH/2, HEIGHT/2-100], 0, amount_of_rays, False)
    #     p.net = copy.deepcopy(bP.net)
    #     p.net.randomize_net(.00001)
    #     new_players.append(p)

    bP = Player([WIDTH/2, HEIGHT/2-100], 0, amount_of_rays, False)
    bP.net = copy.deepcopy(best_player.net)
    bP.color = (0, 150, 255, 255)
    global max_laps
    max_laps = bP.times_finished

    new_players.append(bP)

    for i in range(int(mth.ceil((len(players) - 1)*6/8))):
        p = pick_player(players)
        p.net.randomize_net(.1)
        p.dead = False
        new_players.append(p)
    # for i in range(int(((len(players) - 1)/8)):
    #     p1 = pick_player(players)
    #     p2 = pick_player(players)
    #     p3 = cross_players(p1, p2)
    #     p3.dead = False
    #     new_players.append(p3)
    for i in range(int((len(players) - 1)*2/8)):
        new_players.append(Player([WIDTH/2, HEIGHT/2-100], 0, amount_of_rays, False))
        
    players = []
    players = new_players
    return players
    

def get_am_of_life_players(players):
    sum = 0
    for p in players:
        if not p.dead:
            sum += 1
    return sum


def pick_player(players):
    index = 0
    rand = r.random()
    while rand > 0:
        rand -= players[index].fitness
        index += 1
    index -= 1
    child = Player([WIDTH/2, HEIGHT/2-100], 0, amount_of_rays, False)
    child.net = copy.deepcopy(players[index].net)
    return child


def cross_players(p1, p2):
    # make child with net of first parrent
    child = Player([WIDTH/2, HEIGHT/2-100], 0, amount_of_rays, False)
    child.net = copy.deepcopy(p1.net)
    for i in range(len(child.net.nodes)):
        if not i == 0:
            for n in range(len(child.net.nodes[i])):
                node = child.net.nodes[i][n]
                for w in range(len(node.weights)):
                    if r.randint(0,1):
                        weight = p2.net.nodes[i][n].weights[w]
    return child


def calculate_fitness(players):
    sum = 0
    for p in players:
        sum += p.score
    for p in players:
        # p.fitness = (p.check_piont + (len(checkpoints)+1) * p.times_finished) - 0
        p.fitness = p.score
        # (((mth.pow(p.check_piont, 3) * p.score) - p.rot/360) / sum) * am_of_players
        #(mth.pow(p.check_piont, 2) * p.score)
        #p.score / sum


load_track_file(track_file_name)


@window.event
def on_draw():
    # if gen % 10 == 0:
    window.clear()
    label.draw()
    for p in players:
        if not p.dead:
            p.sprite.draw()
            for line in p.boundries:
                    draw_line([ line[0], line[1] ], [ line[2], line[3] ], p.color)
                    pass
            for rp in p.ray_pts:
                # draw_line([p.pos[0], p.pos[1]], [rp[0], rp[1]], (255, 0, 255, 255))
                pass
    for w in walls:
        draw_line(w.start_pos, w.end_pos, w.color)
    for ch in checkpoints:
        draw_line(ch.start_pos, ch.end_pos, ch.color)
    for b in bullets:
        b.sprite.draw()
        for line in b.boundries:
            draw_line([ line[0], line[1] ], [ line[2], line[3] ], b.color)
            pass
    # else:
    #     window.clear()
    #     label.draw()
    

def update(delta_time):
    global gen
    global players
    for i in range(cycles):
        if all_dead(players):
            
            players = repopulate(players)
            gen += 1
            
            gen_table.append(gen-1)
            label.text = (str("gen: " + str(gen) + " players: " + str(len(players)) + " max laps: " + str(max_laps)))

            # plot of fitness and score
            # fig, axs = plt.subplots(2, 1)
            # fig.max_open_warning = 500
            # axs[0].plot(gen_table, avr_fitness_table, gen_table, best_fitness_table)
            # axs[0].set_xlim(0, len(gen_table)-1)
            # axs[0].set_xlabel('gen.')
            # axs[0].set_ylabel('avr. fitness, best fitness')
            # axs[0].grid(True)

            # axs[1].plot(gen_table, avr_score_table, gen_table, best_score_table)
            # axs[1].set_xlim(0, len(gen_table)-1)
            # axs[1].set_xlabel('gen.')
            # axs[1].set_ylabel('avr. score, best score')
            # axs[1].grid(True)
                            
            # if gen % graph_cycles == 0:
            #     fig.tight_layout()
            #     fig.savefig("graph.png")
        
        lps = get_am_of_life_players(players)
        label.text = (str("gen: " + str(gen) + " players: " + str(lps) + " max laps: " + str(max_laps)))

        for p in players:
            if not p.dead:
                p.cast_rays(walls)
                p.set_net_input()
                p.get_dist_to_closest(players)
                p.move(sim_speed)
                bul = p.shoot(bullets)
                if not bul == None:
                    bullets.append(bul)

                p.check_for_hit(walls, checkpoints, bullets)
                p.out_off_bounds(WIDTH, HEIGHT)

        for b in bullets:
            if not b.dead:
                b.move(sim_speed)
                b.check_for_hit(walls)
                b.out_off_bounds(WIDTH, HEIGHT)
            else:
                bullets.remove(b)
                

pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()