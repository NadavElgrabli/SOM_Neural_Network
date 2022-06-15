# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import multiprocessing
import random
import hexalattice
import pygame
from matplotlib.patches import RegularPolygon

import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np
import matplotlib.backends.backend_agg as agg

def genGrid():
    colors = [["#e6f7ff"], ["#99ddff"], ["#33ccff"], ["#6666ff"], ["#0099ff"],
              ["#0066ff"], ["#3366ff"], ["#0044cc"], ["#000099"], ["#000066"],]
    coord = []
    color = (100, 100, 50)
    map_radius = 4
    for q in range(-map_radius, map_radius+1):
        r1 = max(-map_radius, -q - map_radius)
        r2 = min(map_radius, -q + map_radius);
        for r in range(r1, r2+1):
            coord.append([q, r, -q - r])
            print([q, r, -q - r])
            # colors.append(rhinoscriptsytnax.CreateColor(q, r, -q - r) )

    # Horizontal cartesian coords
    hcoord = [c[0] for c in coord]
    print(hcoord)
    # Vertical cartersian coords
    vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in coord]
    print(vcoord)
    for i in range(len(vcoord)):
        temp = vcoord[i]
        vcoord[i] = -hcoord[i]
        hcoord[i] = temp

    fig, ax = plt.subplots(1, figsize=(5, 5))
    ax.set_aspect('equal')

    # Add some coloured hexagons
    for x, y in zip(hcoord, vcoord):
        color = random.choice(colors)[0]

        hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3,
                                 orientation=np.radians(120), facecolor=color,
                                 alpha=0.9, edgecolor='k')
        ax.add_patch(hex)
    ax.scatter(hcoord, vcoord, alpha=0.3)

    plt.show()


FEATURES = [
    'Yamina',
    'Yahadot Hatora',
    'The Joint Party',
    'Zionut Datit',
    'Kachul Lavan',
    'Israel Betinu',
    'Licod',
    'Merez',
    'Raam',
    'Yesh Atid',
    'Shas',
    'Tikva Hadasha',
]

MAX_VOTES_PER_FEATURE = 50000

def load_data():
    with open('Elec_24.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
        return data

def random_sample():
    return {
        feature: random.randint(0, MAX_VOTES_PER_FEATURE) for feature in FEATURES
    }

def prepare_grid():
    grid = []
    for i in range(5):
        grid.append([random_sample() for _ in range(5 + i)])
    for i in range(4):
        grid.append([random_sample() for _ in range(8 - i)])
    return grid


def score(sample):
    """
    score of row in data / pixel in grid
    """
    raise NotImplementedError()

def choose_representetive(data_row, grid):
    data_row_score = score(data_row)
    best_representitive = (-1, -1)
    best_representitive_distance_so_far = MAX_VOTES_PER_FEATURE

    # Start running over all of the pixels in the grid.

    # iterate the rows of grid
    for i, pixels_in_row_i in enumerate(grid):
        # iterate the columns per row
        for j, pixel_in_row_i_column_j in enumerate(pixels_in_row_i):
            pixel_score = score(pixel_in_row_i_column_j)
            distance = abs(pixel_score - data_row_score)
            if distance < best_representitive_distance_so_far:
                best_representitive = (i, j)
                best_representitive_distance_so_far = distance

    return best_representitive

# def get_neighborhood(i, j):
#     if i <= 5:
#         neighbors = {
#             # myself
#             'middle': (i, j),
#
#             # first tier neighbors
#             'up_left': (i - 1, j - 1),
#             'up_right': (i - 1, j),
#             'left': (i, j - 1),
#             'right': (i, j + 1),
#             'down_left': (i + 1, j),
#             'down_right': (i + 1, j + 1),
#
#             # second tier neighbors
#             'up_up_left': (i - 2, j - 2),
#             'up_up_middle': (i - 2, j-1),
#             'up_up_right': (i - 2, j),
#             'up_left_left': (i-1, j-2),
#             'up_right_right': (i-1, j+1),
#             'left_left': (i, j-2),
#             'right_right': (i, j+2),
#             'down_left_left': (i+1, j-1),
#             'down_right_right': (i+1, j+2),
#             'down_down_left': (i+2, j),
#             'down_down_middle': (i+2, j+1),
#             'down_down_right': (i+2, j+2),
#         }
#     else:
#         # complete for the rows after the 5th row
#         neighbors = {
#             # myself
#             'middle': (i, j),
#
#             # first tier neighbors
#             'up_left': (i - 1, j),
#             'up_right': (i - 1, j + 1),
#             'left': (i, j - 1),
#             'right': (i, j + 1),
#             'down_left': (i + 1, j - 1),
#             'down_right': (i + 1, j),
#
#             # second tier neighbors
#             'up_up_left': (i - 2, j),
#             'up_up_middle': (i - 2, j + 1),
#             'up_up_right': (i - 2, j + 2),
#             'up_left_left': (i - 1, j - 1),
#             'up_right_right': (i - 1, j + 2),
#             'left_left': (i, j - 2),
#             'right_right': (i, j + 2),
#             'down_left_left': (i + 1, j - 2),
#             'down_right_right': (i + 1, j + 1),
#             'down_down_left': (i + 2, j - 2),
#             'down_down_middle': (i + 2, j - 1),
#             'down_down_right': (i + 2, j),
#         }
#         pass
#
#     # Remove neighbors outside the grid
#     for k, (n_i, n_j) in neighbors:
#         if n_i < 0 or n_i >= 9 or n_j < 0 or n_j >= len(grid[i]):
#             del neighbors[k]
#
#     return neighbors

def get_neighborhood(i, j , z):
    neighbors = {
        # myself
        'middle': (i, j, z),

        # first tier neighbors
        'up_left': (i, j - 1, z+1),
        'up_right': (i + 1, j-1, z),
        'left': (i-1, j, z+1),
        'right': (i+1, j, z-1),
        'down_left': (i - 1, j+1, z),
        'down_right': (i, j + 1, z-1),

        # second tier neighbors
        'up_up_left': (i, j - 2, z+2),
        'up_up_middle': (i + 1, j-2, z+1),
        'up_up_right': (i + 2, j-2, 0),
        'up_left_left': (i-1, j-1, z+2),
        'up_right_right': (i+2, j-1, z-1),
        'left_left': (i-2, j, z+2),
        'right_right': (i+2, j, z-2),
        'down_left_left': (i-2, j+1, z+1),
        'down_right_right': (i+1, j+1, z-2),
        'down_down_left': (i-2, j+2, z),
        'down_down_middle': (i-1, j+2, z-1),
        'down_down_right': (i, j+2, z-2),
    }

    # Remove neighbors outside the grid
    for k, (n_i, n_j, n_z) in neighbors:
        if n_i < -4 or n_i > 4 or n_j < -4 or n_j > 4 or n_z < -4 or n_z > 4:
            del neighbors[k]

    return neighbors


def correct_neighbor(grid, neighbor_location, i, j, z, row):
    """
    Correct specific neighbor.
    """
    myself = ['middle']
    first_tier_neighbors = ['up_left',
            'up_right',
            'left',
            'right',
            'down_left',
            'down_right']

    second_tier_neighbors = ['up_up_left',
        'up_up_middle',
        'up_up_right',
        'up_left_left',
        'up_right_right',
        'left_left',
        'right_right',
        'down_left_left',
        'down_right_right',
        'down_down_left',
        'down_down_middle',
        'down_down_right']

    # correct the values of the neighbor i, j to be closer to the row's features
    pixel = grid[i][j][z]
    for feature in FEATURES:
        if neighbor_location in myself:

            pixel[feature] += 0.2 * (row[feature] - pixel[feature])

        # correct pixel in feature (miflaga) k to be closer to the row[feature] (data_row)
        if neighbor_location in first_tier_neighbors:
            #TODO: fix calculation
            pixel[feature] += 0.2 * (row[feature] - pixel[feature])
        else:
            pixel[feature] += 0.1 * (row[feature] - pixel[feature])


def correct_pixel_neighborhood(grid, row, pixel_i, pixel_j, pixel_z):
    """
    Correct all the neighbors by calling to correct_neighbor
    """
    neighbors = get_neighborhood(pixel_i, pixel_j, pixel_z)
    for neighbor_location, (i, j, z) in neighbors:
        correct_neighbor(grid, neighbor_location, i, j, row)


MIN_SCORE = 20
def sidplay_grid():
    colors = [["#e6f7ff"], ["#99ddff"], ["#33ccff"], ["#6666ff"], ["#0099ff"],
              ["#0066ff"], ["#3366ff"], ["#0044cc"], ["#000099"], ["#000066"]]
    labels = [['yes'], ['no'], ['yes'], ['no'], ['yes'], ['no'], ['no']]
    coord = []
    color = (100, 100, 50)
    map_radius = 5
    for q in range(-map_radius, map_radius):
        r1 = max(-map_radius, -q - map_radius)
        r2 = min(map_radius, -q + map_radius);
        for r in range(r1, r2):
            coord.append([q, r, -q - r])

    # Horizontal cartesian coords
    hcoord = [c[0] for c in coord]

    # Vertical cartersian coords
    vcoord = [2. * np.sin(np.radians(60)) * (c[1] - c[2]) / 3. for c in coord]

    for i in range(len(vcoord)):
        temp = vcoord[i]
        vcoord[i] = -hcoord[i]
        hcoord[i] = temp

    fig, ax = plt.subplots(1, figsize=(5, 5))
    ax.set_aspect('equal')

    # Add some coloured hexagons
    for x, y, c, l in zip(hcoord, vcoord, colors, labels):
        color = c[0]

        hex = RegularPolygon((x, y), numVertices=6, radius=2. / 3,
                             orientation=np.radians(120), facecolor=color,
                             alpha=0.9, edgecolor='k')
        ax.add_patch(hex)
        # Also add a text label
        ax.text(x, y + 0.2, l[0], ha='center', va='center', size=20)

    ax.scatter(hcoord, vcoord, alpha=0.3)
    ax = fig.gca()
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    plt.pause(0.01)
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    return canvas, raw_data

if __name__ == '__main__':
    data = load_data()
    grid = prepare_grid()
    pygame.init()

    width = 400
    hight = 400
    display_surface = pygame.display.set_mode((width, hight))
    pygame.display.set_caption('Show Text')
    count = 0
    font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render('generation: ' + str(count), True, "pink")
    textRect = text.get_rect()
    textRect.center = (width // 2, 25)
    gridRect = pygame.Rect(50, 50, 350, 350)
    while True:
        display_surface.fill("white")
        text = font.render('generation: ' + str(count), True, "pink")
        display_surface.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.display.update()
            count += 1

    # work = multiprocessing.Process(target=genGrid())

    # while True:
    #     for row in data:
    #         pixel_i, pixel_j = choose_representetive(row, grid)
    #         correct_pixel_neighborhood(row, pixel_i, pixel_j)
    #         pygame.display.update()

    # total_score = calc_total_score()
    # if total_score < MIN_SCORE:
    #     break
