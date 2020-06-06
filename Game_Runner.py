from Game_Files.Game import Game
import pygame as pg
from Game_Files.Config import Cfg


def find_arrow_move(keys_down) -> str:
    if keys_down[pg.K_COMMA]:
        # build wall
        return "WALL"

    elif keys_down[pg.K_PERIOD]:
        # harvest
        return "HARVEST"

    elif keys_down[pg.K_SLASH]:
        # place bomb
        return "BOMB_ACTIVE"

    elif keys_down[pg.K_SEMICOLON]:
        return "BOMB_INACTIVE"

    elif keys_down[pg.K_l]:
        return "HEALTH"

    elif keys_down[pg.K_UP]:
        return "MOVE_UP"

    elif keys_down[pg.K_DOWN]:
        return "MOVE_DOWN"

    elif keys_down[pg.K_RIGHT]:
        return "MOVE_RIGHT"

    elif keys_down[pg.K_LEFT]:
        return "MOVE_LEFT"

    else:
        return ""


def find_wasd_move(keys_down) -> str:
    if keys_down[pg.K_h]:
        # build wall
        return "WALL"

    elif keys_down[pg.K_g]:
        # harvest
        return "HARVEST"

    elif keys_down[pg.K_f]:
        # place bomb
        return "BOMB_ACTIVE"

    elif keys_down[pg.K_r]:
        return "BOMB_INACTIVE"

    elif keys_down[pg.K_t]:
        return "HEALTH"

    elif keys_down[pg.K_w]:
        return "MOVE_UP"

    elif keys_down[pg.K_s]:
        return "MOVE_DOWN"

    elif keys_down[pg.K_d]:
        return "MOVE_RIGHT"

    elif keys_down[pg.K_a]:
        return "MOVE_LEFT"

    else:
        return ""


game = Game()
clock = pg.time.Clock()

while game.outcome == "TBD":
    clock.tick(Cfg.fps)
    keys = pg.key.get_pressed()

    # player1
    p1_action = find_arrow_move(keys)

    # player2
    p2_action = find_wasd_move(keys)

    game.loop(p1_action, p2_action)


print(game.outcome)
