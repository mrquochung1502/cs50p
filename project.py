import pygame
from game import *


def main():
    # Initialize and run the game
    game = Game()
    game.run()


def create_data_folder(folder_path):
    makedirs(folder_path, exist_ok=True)


def get_target_positions(screen_size, target_distance, grid_edge):
    positions = []
    grid_topleft = (screen_size[0] / 2 - (grid_edge / 2 - .5) * target_distance,
                    screen_size[1] / 2 - (grid_edge / 2 - .5) * target_distance)
    for i in range(grid_edge):
        for j in range(grid_edge):
            x_pos = grid_topleft[0] + target_distance * j
            y_pos = grid_topleft[1] + target_distance * i
            positions.append((x_pos, y_pos))
    return grid_topleft, positions


def load_json(file_path, default=None):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return default


def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    main()
