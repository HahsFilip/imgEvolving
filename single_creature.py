import pygame
from PIL import Image
import numpy as np
import random
import json
"""
IMAGE = Image.open('mona_lisa_small.jpg')
IMAGE.thumbnail((90,60))
IMAGE.save('mona_lisa_even_smaller.jpg', 'JPEG')
TARGET = np.array(IMAGE)
"""
pg_im = pygame.image.load('mona_lisa_even_smaller.jpg')
TARGET = pygame.surfarray.array3d(pg_im)
SIZE = pg_im.get_size()
SHAPE = TARGET.shape
print(SIZE
      )
print(TARGET.shape)
CIRCLES = 70
ACCURACY = 1


def genome_to_array(genome):
    pgim = pygame.Surface(SIZE, pygame.SRCALPHA)
    for circle in genome:
        new_im = pygame.Surface((circle[2] * 2, circle[2] * 2), pygame.SRCALPHA)
        color = circle[0].copy()
        color.append(circle[3])
        pygame.draw.circle(new_im, color, (circle[2], circle[2]), circle[2])
        pgim.blit(new_im, [circle[1][i] - circle[2] for i in range(2)])
    return pygame.surfarray.array3d(pgim)


def random_genome():
    result = []
    for i in range(CIRCLES):
        pos = [random.randint(0, SIZE[0]-1), random.randint(0, SIZE[1]-1)]
        color = [random.randint(0, 255) for i in range(3)]
        radius = random.randint(1, 30)
        opacity = random.randint(0,255)
        result.append([color, pos, radius, opacity])
    return result


def check_fitness(genome):
    genome_array = genome_to_array(genome)
    fitness = (sum(abs(TARGET - genome_array).flat) ** 2) * -1
    return fitness


def check_fitness3(genome):
    genome_array = genome_to_array(genome)
    fitness = (sum(abs(genome_array - TARGET).flat) ** 2) * -1
    return fitness


def check_fitness2(genome):
    genome_array = genome_to_array(genome)
    w, h, d = TARGET.shape
    target2 = TARGET.reshape(w * h, d)
    genome2 = genome_array.reshape(w * h, d)
    fitness = (sum(abs(genome2 - target2).flat) ** 2) * -1
    return fitness


def draw_creature(genome):
    pgim = pygame.Surface((SIZE[0], SIZE[1]), pygame.SRCALPHA)
    for circle in genome:
        new_im = pygame.Surface((circle[2] * 2, circle[2] * 2), pygame.SRCALPHA)
        color = circle[0].copy()
        color.append(circle[3])
        pygame.draw.circle(new_im, color, (circle[2], circle[2]), circle[2])
        pgim.blit(new_im, [circle[1][i] - circle[2] for i in range(2)])
    pg_stringim = pygame.image.tostring(pgim, 'RGBA')
    im = Image.frombytes('RGBA', (SIZE[0], SIZE[1]), pg_stringim)
    im.show()


def mutate(start_genome):
    genome = start_genome.copy()
    repeat = True
    while repeat:
        choice = random.randint(1, 5)
        if choice == 1:
            genome[random.randint(0, CIRCLES - 1)][0] = [random.randint(0, 255) for i in range(3)]
        elif choice == 2:
            genome[random.randint(0, CIRCLES - 1)][1] = [random.randint(0, SIZE[0] - 1),
                                                         random.randint(0, SIZE[1] - 1)]
        elif choice == 3:
            genome[random.randint(0, CIRCLES - 1)][2] = random.randint(1,30)
        elif choice == 4:
            index1 = random.randint(0, CIRCLES-1)
            index2 = random.randint(0, CIRCLES-1)
            while index1 == index2:
                index2 = random.randint(0, CIRCLES - 1)
            temp = genome[index1]
            genome[index1] = genome[index2]
            genome[index2] = temp
        elif choice == 5:
            genome[random.randint(0, CIRCLES - 1)][3] = random.randint(0,255)
        repeat = not random.randint(0, 9)
    return genome


if __name__ == '__main__':
    creature = random_genome()
    """
    improvements = 0
    for i in range(10000):
        print(i)
        kid = mutate(creature)
        if check_fitness(creature) < check_fitness(kid):
            creature = kid
            improvements += 1
    IMAGE.show()
    draw_creature(creature)
    print(improvements)
    """
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


