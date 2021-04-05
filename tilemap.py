import pygame as pg
from SettingsTiled import *
import pytmx

class Map:
    def __init__(self, filename):
        self.Map = []
        with open(filename, 'rt') as f:
            for line in f:
                self.Map.append(line)

        self.tilewidth = len(self.Map[0])
        self.tileheight= len(self.Map)
        self.width = self.tilewidth * tilesize
        self.height = self.tileheight * tilesize
        
class Tilemap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.tileheight * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface





class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = 0
        x = min(0, x)
        self.camera = pg.Rect(x, y, self.width, self.height)
