# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import random

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

MAX_VOTES_PER_FEATURE = 10000

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

def get_neighborhood(i, j):
    if i <= 5:
        neighbors = {
            'middle': (i, j),
            'up_left' : (i - 1, j - 1),
            'up_right' : (i - 1, j),
            'left' : (i, j -1),
            'right' : (i, j + 1),
            'down_left' : (i + 1, j - 1),
            'down_right' : (i + 1, j),
        }
    else:
        # complete for the rows after the 5th row
        pass

    # Remove neighbors outside the grid
    for k, (n_i, n_j) in neighbors:
        if n_i < 0 or n_i >= 9 or n_j < 0 or n_j >= len(grid[i]):
            del neighbors[k]

    return neighbors


def correct_neighbor(grid, neighbor_location, i, j, row):
    """
    Correct specific neighbor.
    """

    first_tier_neighbors = ['up_left', '...', 'down_right']
    second_tier_neighbors = ['up_up_left', '...', 'down_down_right']

    # correct the values of the neighbor i, j to be closer to the row's features
    pixel = grid[i][j]
    for feature in FEATURES:
        #TODO: add fix for mysefl by 30%

        # correct pixel in feature (miflaga) k to be closer to the row[feature]
        if neighbor_location in first_tier_neighbors:
            #TODO: fix calculation
            pixel[feature] += 0.2 * (row[feature] - pixel[feature])
        else:
            pixel[feature] += 0.1 * (row[feature] - pixel[feature])


def correct_pixel_neighborhood(grid, row, pixel_i, pixel_j):
    """
    Correct all the neighbors by calling to correct_neighbor
    """
    neighbors = get_neighborhood(pixel_i, pixel_j)
    for neighbor_location, (i, j) in neighbors:
        correct_neighbor(grid, neighbor_location, i, j, row)


MIN_SCORE = 20

if __name__ == '__main__':
    data = load_data()
    grid = prepare_grid()

    while True:
        for row in data:
            pixel_i, pixel_j = choose_representetive(row, grid)
            correct_pixel_neighborhood(row, pixel_i, pixel_j)

        total_score = calc_total_score()
        if total_score < MIN_SCORE:
            break



