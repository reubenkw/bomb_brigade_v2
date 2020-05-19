from Game import Game
import pygame as pg
from Config import Cfg

game = Game()
clock = pg.time.Clock()

while game.outcome == "TBD":
    clock.tick(Cfg.fps)
    # print(clock.get_fps())

    p1_action = ""
    p2_action = ""

    keys = pg.key.get_pressed()

    # player1
    if keys[pg.K_COMMA]:
        # build wall
        p1_action = "WALL"

    elif keys[pg.K_PERIOD]:
        # harvest
        p1_action = "HARVEST"

    elif keys[pg.K_SLASH]:
        # place bomb
        p1_action = "BOMB_ACTIVE"

    elif keys[pg.K_SEMICOLON]:
        p1_action = "BOMB_INACTIVE"

    elif keys[pg.K_l]:
        p1_action = "HEALTH"

    elif keys[pg.K_UP]:
        p1_action = "MOVE_UP"

    elif keys[pg.K_DOWN]:
        p1_action = "MOVE_DOWN"

    elif keys[pg.K_RIGHT]:
        p1_action = "MOVE_RIGHT"

    elif keys[pg.K_LEFT]:
        p1_action = "MOVE_LEFT"

    # player2
    if keys[pg.K_h]:
        # build wall
        p2_action = "WALL"

    elif keys[pg.K_g]:
        # harvest
        p2_action = "HARVEST"

    elif keys[pg.K_f]:
        # place bomb
        p2_action = "BOMB_ACTIVE"

    elif keys[pg.K_r]:
        p2_action = "BOMB_INACTIVE"

    elif keys[pg.K_t]:
        p2_action = "HEALTH"

    elif keys[pg.K_w]:
        p2_action = "MOVE_UP"

    elif keys[pg.K_s]:
        p2_action = "MOVE_DOWN"

    elif keys[pg.K_d]:
        p2_action = "MOVE_RIGHT"

    elif keys[pg.K_a]:
        p2_action = "MOVE_LEFT"

    game.loop(p1_action, p2_action)

print(game.outcome)
