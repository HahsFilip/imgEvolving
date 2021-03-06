import pygame
from PIL import Image
import numpy as np
import random
import json
from copy import deepcopy
"""
IMAGE = Image.open('mona_lisa_small.jpg')
IMAGE.thumbnail((90,60))
IMAGE.save('mona_lisa_even_smaller.jpg', 'JPEG')
TARGET = np.array(IMAGE)
"""
pg_im = pygame.image.load('mona_lisa_even_smaller.jpg')   # #load target image
TARGET = pygame.surfarray.array3d(pg_im).astype('int16')  # #convert to int16 array
SIZE = pg_im.get_size()
SHAPE = TARGET.shape
print(SIZE
      )
print(TARGET.shape)
CIRCLES = 70
ACCURACY = 1  # #obsolete(?)


def genome_to_array(genome):
    pgim = pygame.Surface(SIZE, pygame.SRCALPHA)
    for circle in genome:
        new_im = pygame.Surface((circle[2] * 2, circle[2] * 2), pygame.SRCALPHA)  #create a surface of size of the circle
        color = circle[0].copy()
        color.append(circle[3])  # #add opacity to the color argument
        pygame.draw.circle(new_im, color, (circle[2], circle[2]), circle[2])  # #draw circle in the middle
        pgim.blit(new_im, [circle[1][i] - circle[2] for i in range(2)])  # #blit onto main surface
    return pygame.surfarray.array3d(pgim).astype('int16')  # #return as int16 array


def random_genome():
    """creates a random genome"""
    result = []
    for i in range(CIRCLES):
        pos = [random.randint(0, SIZE[0]-1), random.randint(0, SIZE[1]-1)]
        color = [random.randint(0, 255) for i in range(3)]
        radius = random.randint(1, 30)
        opacity = random.randint(0,255)
        result.append([color, pos, radius, opacity])
    return result


def check_fitness(genome):
    """returns genome's fitness counted by difference in rgb values"""
    genome_array = genome_to_array(genome)
    fitness = (sum(abs(TARGET - genome_array).flat) ** 2) * -1
    # #squared for rewarding better creatures, difference is a negative trait, hence * -1
    return fitness


def draw_creature(genome):
    pgim = pygame.Surface((SIZE[0], SIZE[1]), pygame.SRCALPHA)
    for circle in genome:  # #same as in genome_to_array
        new_im = pygame.Surface((circle[2] * 2, circle[2] * 2), pygame.SRCALPHA)
        color = circle[0].copy()
        color.append(circle[3])
        pygame.draw.circle(new_im, color, (circle[2], circle[2]), circle[2])
        pgim.blit(new_im, [circle[1][i] - circle[2] for i in range(2)])
    pg_stringim = pygame.image.tostring(pgim, 'RGBA')
    im = Image.frombytes('RGBA', (SIZE[0], SIZE[1]), pg_stringim)
    im.show()


def mutate(start_genome):
    genome = deepcopy(start_genome)  # #deepcopy is necessary (apparently)
    repeat = True
    while repeat:
        choice = random.randint(1, 5)  # #choose a random mutation
        if choice == 1:  # #redefine color
            genome[random.randint(0, CIRCLES - 1)][0] = [random.randint(0, 255) for i in range(3)]
        elif choice == 2:  # #redefine position
            genome[random.randint(0, CIRCLES - 1)][1] = [random.randint(0, SIZE[0] - 1),
                                                         random.randint(0, SIZE[1] - 1)]
        elif choice == 3:  # #redefine radius
            genome[random.randint(0, CIRCLES - 1)][2] = random.randint(1,30)
        elif choice == 4:  # #swap two circles on z axis
            index1 = random.randint(0, CIRCLES-1)
            index2 = random.randint(0, CIRCLES-1)
            while index1 == index2:
                index2 = random.randint(0, CIRCLES - 1)  # #generate two random indices
            temp = genome[index1]
            genome[index1] = genome[index2]  # #swap them
            genome[index2] = temp
        elif choice == 5:  # #redefine opacity
            genome[random.randint(0, CIRCLES - 1)][3] = random.randint(0,255)
        repeat = not random.randint(0, 9)  # #have 10% chance for another mutation
    return genome


if __name__ == '__main__':
    creature = random_genome()  # #generate starting genome

    improvements = 0
    staring_fitness = check_fitness(creature)
    for i in range(300000):
        if i % 500 == 0:
            print(i, check_fitness(creature))  # #check progress every 500 gens
        kid = mutate(creature)  # #create a mutated kid
        if check_fitness(creature) < check_fitness(kid):  # #replace genome if mutation if beneficial
            creature = kid
            improvements += 1
    # #IMAGE.show()
    draw_creature(creature)
    print('improved {} times'.format(improvements))
    print('starting {}'.format(staring_fitness))
    print('end      {}'.format(check_fitness(creature)))
    """
    show_fitness_errors(creature)
    w,h,d = TARGET.shape
    print(tuple(np.average(TARGET.reshape(w*h, d), axis=0)))
    test = [[[85,72,53], [30, 20], 200, 255]]
    test2 = [[[255,255,255], [45,30], 90, 255]]
    print('creature: {}'.format(check_fitness(creature)))
    print('average:  {}'.format(check_fitness(test)))
    print('aberage2: {}'.format(check_fitness3(test)))
    print('white:    {}'.format(check_fitness(test2)))
    draw_creature(test)
    draw_creature(creature)
    """



