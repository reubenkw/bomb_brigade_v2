import pygame as pg
from Config import Cfg


class Tile:
    terrain_types = ["grass", "burnt", "burning"]
    terrain_images = [pg.transform.scale(pg.image.load("textures/grass.png"), (Cfg.tile_width, Cfg.tile_height)),
                      pg.transform.scale(pg.image.load("textures/burnt.png"), (Cfg.tile_width, Cfg.tile_height)),
                      pg.transform.scale(pg.image.load("textures/burning.png"), (Cfg.tile_width, Cfg.tile_height))]

    item_types = ["none", "wall", "heart", "bomb_inactive", "bomb_active"]
    item_images = [None,
                   pg.transform.scale(pg.image.load("textures/wall.png"), (Cfg.tile_width, Cfg.tile_height)),
                   pg.transform.scale(pg.image.load("textures/heart.png"), (Cfg.tile_width, Cfg.tile_height)),
                   pg.transform.scale(pg.image.load("textures/bomb_inactive.png"), (Cfg.tile_width, Cfg.tile_height)),
                   pg.transform.scale(pg.image.load("textures/bomb_active.png"), (Cfg.tile_width, Cfg.tile_height))]

    def __init__(self, terrain_type, item_type):
        self.terrain = Tile.terrain_types.index(terrain_type)
        self.item = Tile.item_types.index(item_type)

    def get_terrain_type(self):
        return Tile.terrain_types[self.terrain]

    def get_item_type(self):
        return Tile.item_types[self.item]

    # def get_terrain_image(self):
    #     return Tile.terrain_images[self.terrain]
    #
    # def get_item_image(self):
    #     return Tile.item_images[self.item]

    def set_terrain(self, terrain_type):
        self.terrain = Tile.terrain_types.index(terrain_type)

    def set_item(self, item_type):
        self.item = Tile.item_types.index(item_type)

    def draw(self, win, x, y):
        if x >= Cfg.tiles_x or y >= Cfg.tiles_y:
            return

        win.blit(Tile.terrain_images[self.terrain], (x * Cfg.tile_width, y * Cfg.tile_height))

        if self.item != 0:
            win.blit(Tile.item_images[self.item], (x * Cfg.tile_width, y * Cfg.tile_height))

    @staticmethod
    def get_item_image(item):
        index = Tile.item_types.index(item)
        return Tile.item_images[index]
