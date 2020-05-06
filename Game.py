import pygame as pg
from Config import Cfg
from Map import Map
from Player import Player
from Bomb import Bomb


class Game:

    def __init__(self):
        self.tick = 0

        self.player1 = Player(Cfg.tiles_x - 4, Cfg.tiles_y - 4, pg.transform.scale(pg.image.load("textures"
                                                                                                 "/player_blue.png"),
                                                                                   (Cfg.tile_width,
                                                                                    Cfg.tile_height)), "Player1")
        self.player2 = Player(4, 4, pg.transform.scale(pg.image.load("textures/player_red.png"),
                                                       (Cfg.tile_width, Cfg.tile_height)), "Player2")
        self.map = Map([(self.player1.x, self.player1.y), (self.player2.x, self.player2.y)])
        self.bombs = []
        self.win = pg.display.set_mode((Cfg.map_width, Cfg.map_height))
        self.outcome = "TBD"
        pg.display.set_caption("Bomb Brigade")
        pg.init()
        self.map.draw(self.win)

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
        elif action == "BOMB" and player.bombs > 0 and player.get_block_front() != (-1, -1):
            x, y = player.get_block_front()
            if self.map.grid[x][y].get_item_type() == "none":
                self.map.tiles2update.append((x, y))
                self.bombs.append(Bomb(x, y, self.tick))
                self.map.grid[x][y].set_item("bomb_active")
                player.bombs -= 1
        elif action == "WALL" and player.walls > 0 and player.get_block_front() != (-1, -1):
            x, y = player.get_block_front()
            if self.map.grid[x][y].get_item_type() == "none":
                self.map.tiles2update.append((x, y)),
                self.map.grid[x][y].set_item("wall")
                player.walls -= 1
            else:
                x, y = player.get_block_behind()
                if (x, y) != (-1, -1) and self.map.grid[x][y].get_item_type() == "none":
                    self.map.tiles2update.append((player.x, player.y))
                    self.map.tiles2update.append((x, y))
                    self.map.grid[player.x][player.y].set_item("wall")
                    player.x, player.y = x, y
                    player.walls -= 1

    def loop(self, p1_action, p2_action):
        self.tick += 1

        # if self.tick > 1000:
        #     self.outcome = "Tie"

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.outcome = "Tie"

        for bomb in self.bombs:
            if bomb.detonation_tick <= self.tick:
                bomb.explode(self.map, (self.player1, self.player2))
                self.bombs.remove(bomb)

        # if self.player1.health <= 0 and self.player2.health <= 0:
        # 	print("Both " + str(self.player1.name) + " and " + str(self.player2.name) + " died")
        # 	self.game_over = True
        # elif self.player1.health <= 0:
        # 	print(self.player1.name, "died")
        # 	self.outcome = self.player2.name
        # 	self.game_over = True
        # elif self.player2.health <= 0:
        # 	print(self.player2.name, "died")
        # 	self.outcome = self.player1.name
        # 	self.game_over = True

        self.action_interpreter(self.player1, p1_action)
        self.action_interpreter(self.player2, p2_action)

        self.map.update_tiles(self.win)
        self.player1.draw(self.win)
        self.player2.draw(self.win)

        pg.display.update()
