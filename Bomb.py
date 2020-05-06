import math
from Config import Cfg
from Map import Map
from Player import Player
from Tile import Tile


class Bomb:

    expRad = [
        (-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4),
        (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3),
        (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
        (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
        (-4, 0), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
        (-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1),
        (-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2),
        (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3),
        (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4)
    ]

    def __init__(self, x0, y0, crnt_tick):
        self.detonation_tick = crnt_tick + Cfg.bomb_delay
        self.x = x0
        self.y = y0

    def explode(self, game_map: Map, players: Player):
        protected_tiles = []
        for square in Bomb.expRad:
            x, y = square
            x += self.x
            y += self.y

            dx = abs(x - self.x)
            dy = abs(y - self.y)
            crnt_x = self.x + 0.5
            crnt_y = self.y + 0.5
            n = 1 + dx + dy
            x_inc = 1 if (x > self.x) else -1
            y_inc = 1 if (y > self.y) else -1
            error = dx - dy
            dx *= 2
            dy *= 2

            while n > 0:
                if game_map.grid[math.floor(crnt_x)][math.floor(crnt_y)].get_item_type() == "wall" \
                        and (math.floor(crnt_x), math.floor(crnt_y)) != (x, y):
                    protected_tiles.append((x, y))
                    n = 0

                if error > 0:
                    crnt_x += x_inc
                    error -= dy
                else:
                    crnt_y += y_inc
                    error += dx

                n -= 1

        for square in Bomb.expRad:
            xSquare, ySquare = square
            xSquare += self.x
            ySquare += self.y

            if (xSquare, ySquare) not in protected_tiles and Cfg.tiles_x > xSquare >= 0 and Cfg.tiles_y > ySquare >= 0:
                game_map.tiles2update.append((xSquare, ySquare))
                if (xSquare, ySquare) == (self.x, self.y) or game_map.grid[xSquare][ySquare].get_item_type() != "bomb_active":
                    game_map.grid[xSquare][ySquare].set_item("none")
                game_map.grid[xSquare][ySquare].set_terrain("burnt")
                for player in players:
                    dist = math.sqrt((xSquare - player.x) ** 2 + (ySquare - player.y) ** 2)
