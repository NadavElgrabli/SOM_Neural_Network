import sys
from frontend import Grid
import pyautogui
import csv
import random
import numpy as np


# Parameters:
MAX_VOTES_PER_FEATURE = 60000
MIN_SCORE = 20000
MAP_RADIUS = 4
MAX_ITERATIONS = 100
ITERATION = 0

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


def load_data():
    with open('Elec_24.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            for k, v in row.items():
                try:
                    row[k] = int(v)
                except:
                    pass
            data.append(row)
        # data = [row for row in reader]
        return data


def random_sample():
    return {
        feature: random.randint(0, MAX_VOTES_PER_FEATURE) for feature in
        FEATURES
    }


def prepare_grid():
    grid = {}
    for q in range(-MAP_RADIUS, MAP_RADIUS + 1):
        r1 = max(-MAP_RADIUS, -q - MAP_RADIUS)
        r2 = min(MAP_RADIUS, -q + MAP_RADIUS)
        for r in range(r1, r2 + 1):
            grid[(q, r, -q - r)] = random_sample()

    return grid


def distance(row_data, pixel_data):
    """
    score of row in data / pixel in grid
    """
    result = 0
    for feature in FEATURES:
        d = pixel_data[feature] - row_data[feature]
        result += np.sqrt(d * d)
    return result


def choose_representative(data_row, grid):
    best_representative = None
    best_representative_distance_so_far = MAX_VOTES_PER_FEATURE

    # Start running over all of the pixels in the grid.

    for q in range(-MAP_RADIUS, MAP_RADIUS + 1):
        r1 = max(-MAP_RADIUS, -q - MAP_RADIUS)
        r2 = min(MAP_RADIUS, -q + MAP_RADIUS)
        for r in range(r1, r2 + 1):
            coord = (q, r, -q - r)
            pixel_data = grid[coord]
            d = distance(data_row, pixel_data)
            if d < best_representative_distance_so_far or best_representative is None:
                best_representative_distance_so_far = d
                best_representative = coord

    return best_representative


def get_neighborhood(i, j, z):
    def coord(a, b):
        return (a, b, -a - b)

    neighbors = {
        # myself
        'middle': (i, j, z),

        # first tier neighbors
        'up_left': coord(i, j - 1),
        'up_right': coord(i + 1, j - 1),
        'left': coord(i - 1, j),
        'right': coord(i + 1, j),
        'down_left': coord(i - 1, j + 1),
        'down_right': coord(i, j + 1),

        # second tier neighbors
        'up_up_left': coord(i, j - 2),
        'up_up_middle': coord(i + 1, j - 2),
        'up_up_right': coord(i + 2, j),
        'up_left_left': coord(i - 1, j - 1),
        'up_right_right': coord(i + 2, j - 1),
        'left_left': coord(i - 2, j),
        'right_right': coord(i + 2, j),
        'down_left_left': coord(i - 2, j + 1),
        'down_right_right': coord(i + 1, j + 1),
        'down_down_left': coord(i - 2, j),
        'down_down_middle': coord(i - 1, j + 2),
        'down_down_right': coord(i, j + 2),
    }

    # Remove neighbors outside the grid
    to_keep = {}
    for k, (n_i, n_j, n_z) in neighbors.items():
        if n_i < -4 or n_i > 4 or n_j < -4 or n_j > 4 or n_z < -4 or n_z > 4:
            continue
        to_keep[k] = (n_i, n_j, n_z)

    return to_keep


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
    pixel = grid[(i, j, z)]
    for feature in FEATURES:
        if neighbor_location in myself:
            pixel[feature] += 0.3 * (row[feature] - pixel[feature])

        # correct pixel in feature (miflaga) k to be closer to the row[feature] (data_row)
        if neighbor_location in first_tier_neighbors:
            pixel[feature] += 0.2 * (row[feature] - pixel[feature])
        else:
            pixel[feature] += 0.1 * (row[feature] - pixel[feature])


def calc_total_score(data, grid_data):
    total_distances = 0
    for row in data:
        representative_coord = choose_representative(row, grid)
        pixel_data = grid_data[representative_coord]
        total_distances += distance(row, pixel_data)
    return total_distances


def correct_pixel_neighborhood(grid, row, pixel_i, pixel_j, pixel_z):
    """
    Correct all the neighbors by calling to correct_neighbor
    """
    neighbors = get_neighborhood(pixel_i, pixel_j, pixel_z)
    for neighbor_location, (i, j, z) in neighbors.items():
        correct_neighbor(grid, neighbor_location, i, j, z, row)


if __name__ == '__main__':

    data = load_data()
    grid = prepare_grid()
    grid_fe = Grid(grid)  # create frontend object to draw the grid

    while True:
        # correct phase
        colors = {}
        sum = {}
        count = {}
        for row in data:
            coord = choose_representative(row, grid)
            correct_pixel_neighborhood(grid, row, coord[0], coord[1], coord[2])
            # colors[coord] = row["Economic Cluster"]
            print(f"{row['Municipality']}: {coord}")
            if coord in count:
                count[coord] += 1
                sum[coord] += row["Economic Cluster"]
            else:
                count[coord] = 1
                sum[coord] = row["Economic Cluster"]

        for k in sum:
            colors[k] = int(sum.get(k) / count.get(k))

        # Choose color
        # for row in data:
        #     coord = choose_representative(row, grid)


        grid_fe.draw_grid(colors)

        total_score = calc_total_score(data, grid)
        print(f"Iteration: {ITERATION}, total_score: {total_score}")
        if total_score < MIN_SCORE:

            myscreenshot = pyautogui.screenshot()
            myscreenshot.save(r'C:\Users\ereze\OneDrive\Pictures\Screenshots\re.png')
            break
        ITERATION += 1
        if ITERATION >= MAX_ITERATIONS:
            myscreenshot = pyautogui.screenshot()
            myscreenshot.save(r'C:\Users\ereze\OneDrive\Pictures\Screenshots\re.png')
            break
