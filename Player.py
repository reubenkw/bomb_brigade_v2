import pygame as pg
from Config import Cfg
from Map import Map


class Player:
    def __init__(self, x0, y0, image0, name0):
        self.health = Cfg.health_start
        self.walls = Cfg.walls_start
        self.bombs = Cfg.bombs_start
        self.look_dir = 0
        self.x = x0
        self.y = y0
        self.image = image0
        self.name = name0

    def move_up(self, game_map: Map):
        game_map.tiles2update.append((self.x, self.y))
        self.look_dir = 0

        if self.y > 0 and game_map.grid[self.x][self.y - 1].get_item_type() == "none":
            self.y -= 1

    def move_down(self, game_map: Map):
        game_map.tiles2update.append((self.x, self.y))
        self.look_dir = 2

        if self.y < Cfg.tiles_y - 1 and game_map.grid[self.x][self.y + 1].get_item_type() == "none":
            self.y += 1

    def move_left(self, game_map: Map):
        game_map.tiles2update.append((self.x, self.y))
        self.look_dir = 3

        if self.x > 0 and game_map.grid[self.x - 1][self.y].get_item_type() == "none":
            self.x -= 1

    def move_right(self, game_map: Map):
        game_map.tiles2update.append((self.x, self.y))
        self.look_dir = 1

        if self.x < Cfg.tiles_x - 1 and game_map.grid[self.x + 1][self.y].get_item_type() == "none":
            self.x += 1

    def get_block_front(self):
        if self.look_dir == 0 and self.y > 0:
            return self.x, self.y - 1
        elif self.look_dir == 1 and self.x < Cfg.tiles_x - 1:
            return self.x + 1, self.y
        elif self.look_dir == 2 and self.y < Cfg.tiles_y - 1:
            return self.x, self.y + 1
        elif self.look_dir == 3 and self.x > 0:
            return self.x - 1, self.y
        else:
            return -1, -1

    def get_block_behind(self):
        if self.look_dir == 0 and self.y < Cfg.tiles_y - 1:
            return self.x, self.y + 1
        elif self.look_dir == 1 and self.x > 0:
            return self.x - 1, self.y
        elif self.look_dir == 2 and self.y > 0:
            return self.x, self.y - 1
        elif self.look_dir == 3 and self.x < Cfg.tiles_x - 1:
            return self.x + 1, self.y
        else:
            return -1, -1

    def harvest(self, game_map: Map):
        x, y = self.get_block_front()
        game_map.tiles2update.append((x, y))

        tile_resource = game_map.grid[x][y].get_item_type()
        if tile_resource == "bomb_inactive" and self.bombs < Cfg.bombs_max:

            self.bombs += 1
            game_map.grid[x][y].set_item("none")
        elif tile_resource == "wall" and self.walls < Cfg.walls_max:

            self.walls += 1
            game_map.grid[x][y].set_item("none")
        elif tile_resource == "heart" and self.health < Cfg.health_max:

            self.health += 1
            game_map.grid[x][y].set_item("none")

    def draw(self, win):
        image = self.image
        win.blit(pg.transform.rotate(image, - 90 - 90 * self.look_dir), (self.x * Cfg.tile_width, self.y * Cfg.tile_height))

    def print(self):
        print(str(self.name) + "[Health: " + str(self.health) + ", Bombs: "
              + str(self.bombs) + ", Walls: " + str(self.walls) + "]")
