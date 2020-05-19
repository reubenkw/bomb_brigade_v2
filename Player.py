import pygame as pg
from Config import Cfg
from Map import Map
from Tile import Tile


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
        self.last_burning = 0

        # for info display optimization
        self.update_info = True

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

            # for info display optimization
            self.update_info = True
        elif tile_resource == "wall" and self.walls < Cfg.walls_max:

            self.walls += 1
            game_map.grid[x][y].set_item("none")

            # for info display optimization
            self.update_info = True
        elif tile_resource == "heart" and self.health < Cfg.health_max:

            self.health += 1
            game_map.grid[x][y].set_item("none")

            # for info display optimization
            self.update_info = True

    def draw(self, win):
        win.blit(pg.transform.rotate(self.image, - 90 - 90 * self.look_dir),
                 (self.x * Cfg.tile_width, self.y * Cfg.tile_height))

    def display_stats(self, win, position, colour):

        text_spacing = 65
        font = pg.font.SysFont(None, 60)

        spacing = 16
        image_scaling = 2
        image_size = Cfg.tile_width * image_scaling

        # PlayerName
        # Health Icons (5x1 max)
        # Bomb Icons (5x1 max)
        # Wall Icons (5x3 max)

        x, y = position
        x += spacing
        y += spacing
        font = pg.font.SysFont(None, 32)
        text = font.render(self.name, True, pg.Color(colour))
        win.blit(text, (x, y))

        def draw_row(icon, num, pos):
            crnt_x, crnt_y = pos
            for _ in range(num):
                win.blit(icon, (crnt_x, crnt_y))
                crnt_x += image_size + spacing

        x, y = position
        x += spacing
        y += spacing * 2 + image_size
        image = pg.transform.scale(Tile.get_item_image("heart"), (image_size, image_size))
        draw_row(image, self.health, (x, y))

        x, y = position
        x += spacing
        y += spacing * 3 + image_size * 2
        image = pg.transform.scale(Tile.get_item_image("bomb_inactive"), (image_size, image_size))
        draw_row(image, self.bombs, (x, y))

        x, y = position
        x += spacing * 6 + image_size * 5
        y += spacing
        image = pg.transform.scale(Tile.get_item_image("wall"), (image_size, image_size))
        for row in range(int(self.walls / 5) + 1):
            draw_row(image, min(5, self.walls - row * 5), (x, y))

            y += image_size + spacing

    def check_burning(self, game_map: Map):

        if game_map.grid[self.x][self.y].get_terrain_type() == "burning" and self.last_burning > Cfg.burning_delay:
            self.last_burning = 0
            self.health -= 1

            # for info display optimization
            self.update_info = True
        else:
            self.last_burning += 1

    # Used for debugging
    def print(self):
        print(str(self.name) + "[Health: " + str(self.health) + ", Bombs: "
              + str(self.bombs) + ", Walls: " + str(self.walls) + "]")
