##################################################################
# Title:    Game of War V1
# Author:   Preston Brubaker
# Revision: 7/25/23
#################################################################
import random
# Import libraries
import time
use_pygame = True
if use_pygame: import pygame





# Variables

time_between_its = 0
max_its = 10000000000
pause_int = 50000000000


window_size_x = 1800             # Width of window
window_size_y = 900             # Height of window
show_text = False
draw_grid = True
show_org_info = True
chance_org_info = .000001

grid_s_x = 100                    # Number of pixels in x-direciton
grid_s_y = 50

# Number of pixels in y-direction
grid_s = grid_s_x * grid_s_y    # Number of pixels

border_w = 2 * 0                    # Width of border between pixels

# Calculate the pixel sizes based on the number of pixels in both directions
pixel_s_x = window_size_x / grid_s_x - border_w / 2
pixel_s_y = window_size_y / grid_s_y - border_w / 2

iteration_count = 0

food = []                       # 2D list of food associated with each pixel
food_gen_i = 10
food_gen_rate = 1
is_occupied = []
mut_ch_c = 0.1     # Chance of changing a given gene to a new random number
mut_ins_c = 0.1    # Chance of inserting a gene to the end
mut_rem_c = 0.1    # Chance of removing a random gene

    # Organisms
org_c_i = int(grid_s_x * grid_s_y * .3)    # Number of initial organisms
rep_req = 100   # Amount of food needed for reproduction
rep_c = 1.0     # Chance of reproduction when able
min_rep_idx = 1 # Minimum index to reproduce
org_info = []   # Array with all the info about each organism
met_rate = 1   #metabolic rate
org_f_i = 20   # Initial reserve of food
org_gen_len_i =  20 # Initial max length of genome
max_genome_len = 20
frac_mut = .01  #maximum mutation fraction
max_a = 14  #maximum value of an allele
max_age = 1000 # Max age


class Organism:
    def __init__(self, id, x, y, genome, food_rsv, indx, org_inf_idx, eat_frac, age, team, team_share_frac):
        self.id = id
        self.x = x
        self.y = y
        self.genome = genome
        self.food_rsv = food_rsv
        self.indx = indx
        self.org_inf_idx = org_inf_idx
        self.eat_frac = eat_frac
        self.age = age
        self.team = team
        self.team_share_frac = team_share_frac

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def print_info(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("ID: ", self.id)
        print(f"Position: ({self.x}, {self.y})")
        print("Genome: ", self.genome)
        print("Food Reserve: ", round(self.food_rsv, 1))
        print("Index: ", self.indx)
        print("Index in org_inf: " , self.org_inf_idx)
        print("Eating fraction: ", round(self.eat_frac, 2))
        print("Age: ", self.age)
        print("Team: ", self.team)
        print("Team share fraction: ", round(self.team_share_frac, 3))







def initialize_food():
    global food
    for x in range(grid_s_x):
        row = []
        for y in range(grid_s_y):
            row.append(food_gen_i)
        food.append(row)

def initialize_is_occupied():
    global is_occupied
    for x in range(grid_s_x):
        row = []
        for y in range(grid_s_y):
            row.append(-1)
        is_occupied.append(row)

def initialize_orgs():
    global org_info
    for i in range(org_c_i):
        id = len(org_info)
        org_inf_idx = id + 1
        x = random.randint(0, grid_s_x - 1)
        y = random.randint(0, grid_s_y - 1)
        genome = []
        len_genome = random.randint(10, org_gen_len_i)
        for j in range(len_genome):
            r1 = random.randint(1,max_a)
            genome.append(r1)
        team = random.randint(0, 255 * 3)
        food_rsv = org_f_i
        indx = 1
        age = 0
        eat_frac = random.uniform(.5,1)
        team_share_frac = random.uniform(0,1)
        org_info.append(Organism(id, x, y, genome, food_rsv, indx, org_inf_idx, eat_frac, age, team, team_share_frac))

def drawGrid():
    if use_pygame: font = pygame.font.Font(None, int(pixel_s_y / 4))  # None means the default system font
    for x in range(grid_s_x):
        for y in range(grid_s_y):
            u = window_size_x / grid_s_x * x
            v = window_size_y / grid_s_y * y
            if use_pygame: pygame.draw.rect(window, (100, 100, 100), (u, v, pixel_s_x, pixel_s_y))
            if (show_text == True):
                #food[x][y]
                if use_pygame: text = font.render(str(int(food[x][y])), True, (255, 255, 255))  # (255, 255, 255) is white color
                if use_pygame: text_position = ((u, v))
                if use_pygame: window.blit(text, text_position)
    for organism in org_info:
        x = window_size_x / grid_s_x * organism.x + border_w / 2
        y = window_size_y / grid_s_y * organism.y + border_w / 2
        genome = organism.genome
        team = organism.team
        color = team
        red = 0
        green = 0
        blue = 0
        if(color <= 255):
            red = color
        if(color > 255 and color <= 255 * 2):
            green = color % 255
        if(color > 255 * 2):
            blue = color % (255 * 2)

        if use_pygame: pygame.draw.rect(window, (red, green, blue), (x, y, pixel_s_x, pixel_s_y))
        if(show_text == True):
            if use_pygame: text = font.render(str(int(is_occupied[organism.x][organism.y])), True, (255, 255, 255))  # (255, 255, 255) is white color
            if use_pygame: text_position = ((x, y))
            if use_pygame: window.blit(text, text_position)
            if use_pygame: text = font.render(str(int(food[organism.x][organism.y])), True, (255, 255, 255))  # (255, 255, 255) is white color
            if use_pygame: text_position = ((x, y + pixel_s_y / 4))
            if use_pygame: window.blit(text, text_position)
            if use_pygame: text = font.render(str(int(organism.food_rsv)), True, (255, 255, 255))  # (255, 255, 255) is white color
            if use_pygame: text_position = ((x, y + pixel_s_y / 4 * 2))
            if use_pygame: window.blit(text, text_position)
    if use_pygame: font = pygame.font.Font(None, int(16))  # None means the default system font
    if use_pygame: text = font.render(str(int(iteration_count)), True, (0, 255, 0))  # (255, 255, 255) is white color
    if use_pygame: text_position = ((10,10))
    if use_pygame: window.blit(text, text_position)

def reproduce(x, y, food_trans, organism):
    global org_c_i
    indx = 0
    id = org_c_i - 1
    age = 0
    offspring_food_rsv = food_trans  # Assign the food_trans to the offspring
    # Use the list's copy() method to create a copy of the genome
    genome = organism.genome.copy()



    # Mutations
    team = organism.team
    for i in range(len(genome)):
        r1 = random.uniform(0,1)
        if(r1 < mut_ch_c):
            r2 = random.randint(1,max_a)
            genome[i] = r2

    if(random.uniform(0,1) < .2):
        r3 = random.uniform(0,1)
        if(r3 > .5):
            team +=1
        if(r3 < .5):
            team -=1


    if(team < 0):
        team = 255 * 3
    if(team > 255 * 3):
        team = 20

    r1 = random.uniform(0,1)
    r2 = random.randint(1,max_a)
    if(r1 < mut_ins_c and len(genome) < max_genome_len):
        genome.append(r2)

    r1 = random.uniform(0, 1)
    r2 = random.randint(0, len(genome) - 1)
    if (r1 < mut_rem_c and len(genome) > 5):
       genome.pop(r2)

    eat_frac = organism.eat_frac * (random.uniform(1-frac_mut, 1+frac_mut))
    team_share_frac = organism.team_share_frac * (random.uniform(1-frac_mut, 1+frac_mut))
    if(eat_frac > 1):
        eat_frac = 1
    if(team_share_frac > 1):
        team_share_frac = 1
    org_inf_idx = len(org_info) - 1
    team_share_frac = organism.team_share_frac
    org_info.append(Organism(id, x, y, organism.genome, offspring_food_rsv, indx, org_inf_idx, eat_frac, age, team, team_share_frac))
    org_c_i += 1




def update_org():
    global org_info
    death_note = []
    for organism in org_info:
        idx = organism.indx
        genome = organism.genome
        if(idx > len(genome) - 1):
            idx = 0
            organism.indx = 1

        instruction = genome[idx]
        x = organism.x
        y = organism.y

        team = genome[0]

        # Eat
        food_trans = food[x][y] * organism.eat_frac
        organism.food_rsv += food_trans
        food[x][y] -= food_trans

        # Metabolism
        organism.food_rsv -= met_rate

        # Share with teammates
        food_shared = organism.food_rsv * organism.team_share_frac
        if (x < grid_s_x - 1):
            if (is_occupied[x + 1][y] > team - 20 and is_occupied[x + 1][y] < team + 20):
                organism2 = org_info[is_occupied[x + 1][y]]
                organism2.food_rsv += food_shared
                organism.food_rsv -= food_shared

        if (y > 0):
            if (is_occupied[x][y - 1] > team - 20 and is_occupied[x][y - 1] < team + 20):
                organism2 = org_info[is_occupied[x][y - 1]]
                organism2.food_rsv += food_shared
                organism.food_rsv -= food_shared

        if (x > 0):
            if (is_occupied[x - 1][y] > team - 20 and is_occupied[x - 1][y] < team + 20):
                organism2 = org_info[is_occupied[x - 1][y]]
                organism2.food_rsv += food_shared
                organism.food_rsv -= food_shared

        if (y < grid_s_y - 1):
            if (is_occupied[x][y + 1] > team - 20 and is_occupied[x][y + 1] < team + 20):
                organism2 = org_info[is_occupied[x][y + 1]]
                organism2.food_rsv += food_shared
                organism.food_rsv -= food_shared

        # Write the death note >:)
        if(organism.food_rsv < 0 or instruction == -9 or organism.age / max_age > random.uniform(0,1)):
            death_note.append(organism)
            if(organism.food_rsv > 0):
                food[x][y] += organism.food_rsv * 1.5
                organism.food_rsv = 0

        # Reproduce
        if(idx >= min_rep_idx and rep_c >= random.uniform(0,1)):
            if (instruction == 5 and x < grid_s_x - 1):
                if (is_occupied[x + 1][y] == -1):
                    food_trans = organism.food_rsv * 0.5
                    organism.food_rsv -= food_trans
                    reproduce(x + 1, y, food_trans, organism)
            if (instruction == 6 and y > 0):
                if (is_occupied[x][y - 1] == -1):
                    food_trans = organism.food_rsv * 0.5
                    organism.food_rsv -= food_trans
                    reproduce(x, y - 1, food_trans, organism)
            if (instruction == 7 and x > 0):
                if (is_occupied[x - 1][y] == -1):
                    food_trans = organism.food_rsv * 0.5
                    organism.food_rsv -= food_trans
                    reproduce(x - 1, y, food_trans, organism)
            if (instruction == 8 and y < grid_s_y - 1):
                if (is_occupied[x][y + 1] == -1):
                    food_trans = organism.food_rsv * 0.5
                    organism.food_rsv -= food_trans
                    reproduce(x, y + 1, food_trans, organism)

        # Eat others
        if (x < grid_s_x - 1 and instruction == 11):
            if (is_occupied[x + 1][y] < team - 20 and is_occupied[x + 1][y] > team + 20):
                organism2 = org_info[is_occupied[x + 1][y]]
                food_taken = organism2.food_rsv * .5
                organism2.food_rsv -= food_taken
                organism.food_rsv += food_taken

        if (y > 0 and instruction == 12):
            if (is_occupied[x][y - 1] < team - 20 and is_occupied[x][y - 1] > team + 20):
                organism2 = org_info[is_occupied[x][y - 1]]
                food_taken = organism2.food_rsv * .5
                organism2.food_rsv -= food_taken
                organism.food_rsv += food_taken

        if (x > 0 and instruction == 13):
            if (is_occupied[x - 1][y] < team - 20 and is_occupied[x - 1][y] > team + 20):
                organism2 = org_info[is_occupied[x - 1][y]]
                food_taken = organism2.food_rsv * .5
                organism2.food_rsv -= food_taken
                organism.food_rsv += food_taken

        if (y < grid_s_y - 1 and instruction == 14):
            if (is_occupied[x][y + 1] < team - 20 and is_occupied[x][y + 1] > team + 20):
                organism2 = org_info[is_occupied[x][y + 1]]
                food_taken = organism2.food_rsv * .5
                organism2.food_rsv -= food_taken
                organism.food_rsv += food_taken





        # Move organism
        if(instruction == 1 and x < grid_s_x - 1):
            if (is_occupied[x + 1][y] == -1):
                organism.move(x + 1, y)
        if (instruction == 2 and y > 0):
            if (is_occupied[x][y - 1] == -1):
                organism.move(x, y - 1)
        if (instruction == 3 and x > 0):
            if (is_occupied[x - 1][y] == -1):
                organism.move(x - 1, y)
        if (instruction == 4 and y < grid_s_y - 1):
            if(is_occupied[x][y + 1] == -1):
                organism.move(x, y + 1)

        organism.indx += 1
        organism.age += 1

    # Kill the weak
    for organism in death_note:
        org_info.remove(organism)






def update_occupation():
    for x in range(grid_s_x):
        for y in range(grid_s_y):
            is_occupied[x][y] = -1

    for organism in org_info:
        x = organism.x
        y = organism.y
        is_occupied[x][y] = org_info.index(organism)

def add_food():
    for x in range(grid_s_x):
        for y in range(grid_s_y):
            if is_occupied[x][y] == -1:
                food[x][y] += food_gen_rate





# Initialize
    # Pygame
if use_pygame: pygame.init()
if use_pygame: window = pygame.display.set_mode((window_size_x,window_size_y))

initialize_food()
initialize_is_occupied()
initialize_orgs()

    # Debugging


running = True
while running and iteration_count < max_its:
    if use_pygame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    iteration_count += 1
    if use_pygame: window.fill((0, 0, 0))  # Clear display


    drawGrid()  # Draw grid

    # Debugging
    if(show_org_info == True):
        for organism in org_info:
            if(random.uniform(0,1) < chance_org_info):
                organism.print_info()



    if use_pygame: pygame.display.flip()   # Update display

    if iteration_count > 1:
        time.sleep(time_between_its)

    if(iteration_count % pause_int == 0):
        print("Chance of mutation: " + str(mut_ch_c))
        print("Chance of ins/rem: " + str(mut_ins_c))
        print("Food gen rate: " + str(food_gen_rate))
        print("frac mut rate: " + str(frac_mut))
        print("time between intervals: " + str(time_between_its))
        pause_int = int(input("Next Interval: "))
        mut_ch_c = float(input("Chance of mutation: "))
        mut_ins_c = float(input("Chance of insertion / removal: "))
        mut_rem_c = mut_ch_c
        food_gen_rate = float(input("Food Gen rate: "))
        eat_frac_mut = float(input("Fractional mut rate: "))
        time_between_its = float(input("Time between intervals: "))


    update_org()
    update_occupation()
    add_food()

if use_pygame: pygame.quit()