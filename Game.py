import math
import shutil

import pygame as pg
from Config import Cfg
from Map import Map
from Player import Player
from Bomb import Bomb
import os


class Game:

    def __init__(self):
        self.tick = 0

        self.player1 = Player(Cfg.tiles_x - 5, Cfg.tiles_y - 5, pg.transform.scale(pg.image.load("textures"
                                                                                                 "/player_blue.png"),
                                                                                   (Cfg.tile_width,
                                                                                    Cfg.tile_height)), "Player1")
        self.player2 = Player(4, 4, pg.transform.scale(pg.image.load("textures/player_red.png"),
                                                       (Cfg.tile_width, Cfg.tile_height)), "Player2")
        self.map = Map([(self.player1.x, self.player1.y), (self.player2.x, self.player2.y)])
        self.bombs = []
        self.win = pg.display.set_mode((Cfg.win_width, Cfg.win_height))
        self.outcome = "TBD"
        pg.display.set_caption("Bomb Brigade")
        pg.init()
        self.map.draw(self.win)

        pg.draw.rect(self.win, pg.Color('grey'), pg.Rect((0, Cfg.map_height), (Cfg.win_width, Cfg.info_height)))
        self.player1.display_stats(self.win, (Cfg.map_width - 496, Cfg.map_height), "blue")
        self.player2.display_stats(self.win, (0, Cfg.map_height), "red")

        if Cfg.output_images:
            Game.reset_images()

    def action_interpreter(self, player, action):
        if action == "MOVE_UP":
            player.move_up(self.map)
        elif action == "MOVE_DOWN":
            player.move_down(self.map)
        elif action == "MOVE_LEFT":
            player.move_left(self.map)
        elif action == "MOVE_RIGHT":
            player.move_right(self.map)
        elif action == "HARVEST" and player.get_block_front() != (-1, -1):
            player.harvest(self.map)
        elif action == "BOMB_ACTIVE" and player.bombs > 0 and player.get_block_front() != (-1, -1):
            x, y = player.get_block_front()
            if self.map.grid[x][y].get_item_type() == "none":
                self.map.tiles2update.append((x, y))
                self.bombs.append(Bomb(x, y, self.tick))
                self.map.grid[x][y].set_item("bomb_active")
                player.bombs -= 1

                # for info display optimization
                player.update_info = True
        elif action == "WALL" and player.walls > 0 and player.get_block_front() != (-1, -1):
            x, y = player.get_block_front()
            if self.map.grid[x][y].get_item_type() == "none":
                self.map.tiles2update.append((x, y)),
                self.map.grid[x][y].set_item("wall")
                player.walls -= 1

                if self.map.grid[x][y].get_terrain_type() == "burning":
                    self.map.grid[x][y].set_terrain("burnt")

                # for info display optimization
                player.update_info = True
            else:
                x, y = player.get_block_behind()
                if (x, y) != (-1, -1) and self.map.grid[x][y].get_item_type() == "none":
                    self.map.tiles2update.append((player.x, player.y))
                    self.map.tiles2update.append((x, y))
                    self.map.grid[player.x][player.y].set_item("wall")
                    player.x, player.y = x, y
                    player.walls -= 1

                    # for info display optimization
                    player.update_info = True
        elif action == "HEALTH":
            x, y = player.get_block_front()
            if self.map.grid[x][y].get_item_type() == "none" and player.health > 1:
                self.map.tiles2update.append((x, y))
                self.map.grid[x][y].set_item("heart")
                player.health -= 1

                # for info display optimization
                player.update_info = True
        elif action == "BOMB_INACTIVE":
            x, y = player.get_block_front()
            if self.map.grid[x][y].get_item_type() == "none" and player.bombs > 0:
                self.map.tiles2update.append((x, y))
                self.map.grid[x][y].set_item("bomb_inactive")
                player.bombs -= 1

                # for info display optimization
                player.update_info = True

    @staticmethod
    def reset_images():
        shutil.rmtree("images", ignore_errors=True)
        os.makedirs("images")

    def save_screen(self):
        file = "images/" + str(self.tick) + ".png"
        pg.image.save(self.win, file)

    def display_tick(self):
        pg.draw.rect(self.win, pg.Color('grey'), pg.Rect((496, Cfg.map_height), (Cfg.win_width - 2 * 496, Cfg.info_height)))

        font = pg.font.SysFont(None, 32)
        text = font.render(str(math.floor(self.tick / 10)), True, pg.Color("black"))
        text_width, text_height = font.size(str(math.floor(self.tick / 10)))
        self.win.blit(text, (int((Cfg.win_width - text_width) / 2), Cfg.map_height + 32))

    def loop(self, p1_action, p2_action):
        self.tick += 1
        self.player1.update_info = False
        self.player2.update_info = False

        # if self.tick > 1000:
        #     self.outcome = "Tie"

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.outcome = "Tie"

        for bomb in self.bombs:
            if bomb.detonation_tick <= self.tick:
                bomb.explode(self.map, (self.player1, self.player2), self.bombs, self.tick)

        if self.player1.health <= 0 and self.player2.health <= 0:
            self.outcome = "Tie"
        elif self.player1.health <= 0:
            self.outcome = "Player2 won"
        elif self.player2.health <= 0:
            self.outcome = "Player1 won"

        self.action_interpreter(self.player1, p1_action)
        self.action_interpreter(self.player2, p2_action)

        self.map.update_tiles(self.win)

        if not self.tick % Cfg.bomb_spawn_rate:
            self.map.resource_gen_spot("bomb_inactive", 1, [(self.player1.x, self.player1.y),
                                                            (self.player2.x, self.player2.y)])

        self.player1.check_burning(self.map)
        self.player2.check_burning(self.map)

        if self.tick > Cfg.border_shrink_delay and self.tick % Cfg.border_shrink_rate:
            self.map.shrink_border(int((self.tick - Cfg.border_shrink_delay) / Cfg.border_shrink_rate))

        self.player1.draw(self.win)
        self.player2.draw(self.win)

        if self.player1.update_info:
            pg.draw.rect(self.win, pg.Color('grey'),
                         pg.Rect((Cfg.map_width - 496, Cfg.map_height), (496, Cfg.info_height)))
            self.player1.display_stats(self.win, (Cfg.map_width - 496, Cfg.map_height), "blue")

        if self.player2.update_info:
            pg.draw.rect(self.win, pg.Color('grey'), pg.Rect((0, Cfg.map_height),
                                                             (496, Cfg.info_height)))
            self.player2.display_stats(self.win, (0, Cfg.map_height), "red")

        pg.display.update()
        self.display_tick()

        if Cfg.output_images:
            self.save_screen()
