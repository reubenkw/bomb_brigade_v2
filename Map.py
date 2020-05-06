import pygame as pg
import random
from Config import Cfg
from Tile import Tile


class Map:

    def __init__(self, player_positions):
        self.grid = [[Tile("grass", "none") for _ in range(Cfg.tiles_y)] for _ in range(Cfg.tiles_x)]
        self.tiles2update = []

        self.resource_gen(Cfg.walls_num_deposit, Cfg.walls_deposit_size, player_positions)

        for _ in range(Cfg.bombs_num_deposit):
            x, y = self.rand_empty_pos(player_positions)
            if (x, y) != (-1, -1):
                self.grid[x][y].set_item("bomb_inactive")

        for _ in range(Cfg.health_num_deposit):
            x, y = self.rand_empty_pos(player_positions)
            if (x, y) != (-1, -1):
                self.grid[x][y].set_item("heart")

    def res_recursive(self, pos, prob, not_allowed):
        if pos in not_allowed:
            return

        x, y = pos
        self.grid[x][y].set_item("wall")
        if x < Cfg.tiles_x - 1 and self.grid[x + 1][y].get_item_type() == "none" and random.random() < prob:
            self.res_recursive((x + 1, y), prob - 0.01, not_allowed)
        if y < Cfg.tiles_y - 1 and self.grid[x][y + 1].get_item_type() == "none" and random.random() < prob:
            self.res_recursive((x, y + 1), prob - 0.01, not_allowed)
        if x > 0 and self.grid[x - 1][y].get_item_type() == "none" and random.random() < prob:
            self.res_recursive((x - 1, y), prob - 0.01, not_allowed)
        if y > 0 and self.grid[x][y - 1].get_item_type() == "none" and random.random() < prob:
            self.res_recursive((x, y - 1), prob - 0.01, not_allowed)

    def resource_gen(self, num_deposits, prob, not_allowed):
        for _ in range(num_deposits):
            x, y = self.rand_empty_pos(not_allowed)
            if (x, y) != (-1, -1):
                self.grid[x][y].set_item("wall")
                self.res_recursive((x, y), prob, not_allowed)

    def rand_empty_pos(self, not_allowed):
        tries = 0
        max_tries = 60

        while True:
            x = random.randint(0, Cfg.tiles_x - 1)
            y = random.randint(0, Cfg.tiles_y - 1)

            if self.grid[x][y].get_item_type() == "none" and (x, y) not in not_allowed:
                return x, y
            else:
                tries += 1
                if tries > max_tries:

                    for x in range(Cfg.tiles_x):
                        for y in range(Cfg.tiles_y):
                            if self.grid[x][y].get_item_type() == "none" and (x, y) not in not_allowed:
                                return x, y

                    return -1, -1

    def update_tiles(self, win):
        for x, y in self.tiles2update:
            self.grid[x][y].draw(win, x, y)

        self.tiles2update.clear()

    def draw(self, win):
        for x in range(Cfg.tiles_x):
            for y in range(Cfg.tiles_y):
                self.grid[x][y].draw(win, x, y)
