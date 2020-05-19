import math
from Config import Cfg
from Map import Map
from Player import Player
from Tile import Tile


class Bomb:
    # does not include 0,0
    expRad = [
        (-2, 4), (-1, 4), (0, 4), (1, 4), (2, 4),
        (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3),
        (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
        (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
        (-4, 0), (-3, 0), (-2, 0), (-1, 0),         (1, 0), (2, 0), (3, 0), (4, 0),
        (-4, -1), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1),
        (-4, -2), (-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2),
        (-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3),
        (-2, -4), (-1, -4), (0, -4), (1, -4), (2, -4)
    ]

    def __init__(self, x0, y0, crnt_tick):
        self.detonation_tick = crnt_tick + Cfg.bomb_delay
        self.x = x0
        self.y = y0

    def explode(self, game_map: Map, players: Player, bombs, tick):
        protected_tiles = []
        for square in Bomb.expRad:
            x, y = square
            x += self.x
            y += self.y

            if not (0 <= x < Cfg.tiles_x and 0 <= y < Cfg.tiles_y):
                continue

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
                # print(game_map.grid[math.floor(crnt_x)][math.floor(crnt_y)].get_item_type())
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

        game_map.tiles2update.append((self.x, self.y))
        game_map.grid[self.x][self.y].set_terrain("burning")
        game_map.grid[self.x][self.y].set_item("none")

        bombs.remove(self)
        toExplode = []
        for x, y in Bomb.expRad:
            x += self.x
            y += self.y

            if (x, y) not in protected_tiles and Cfg.tiles_x > x >= 0 and Cfg.tiles_y > y >= 0:
                game_map.tiles2update.append((x, y))

                if game_map.grid[x][y].get_item_type() == "bomb_active" and (x, y) != (self.x, self.y):
                    for bomb in bombs:
                        if (x, y) == (bomb.x, bomb.y):
                            toExplode.append(bomb)
                elif game_map.grid[x][y].get_item_type() == "bomb_inactive":
                    game_map.grid[x][y].set_item("bomb_active")
                    bombs.append(Bomb(x, y, tick))
                else:
                    game_map.grid[x][y].set_item("none")

                if game_map.grid[x][y].get_terrain_type() != "burning":
                    game_map.grid[x][y].set_terrain("burnt")

                for player in players:
                    if (player.x, player.y) == (x, y):
                        player.health -= 1

                        # for info display optimization
                        player.update_info = True

        for bomb in toExplode:
            bomb.explode(game_map, players, bombs, tick)