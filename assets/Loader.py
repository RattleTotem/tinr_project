from pygame import *
import pygame as pg
from config.Settings import *

class Loader:

    def loadTiles(sheet):
        assets = {}
        assets["grass_tile"] = sheet.imageAt((16*5, 0, 16, 16), scale=3)
        assets["dirt_tile"] = sheet.imageAt((16*6, 0, 16, 16), scale=3)
        assets["stone_tile"] = sheet.imageAt((16*5, 0, 16, 16), scale=3)

        return assets

    def loadCharacters(sheet):
        assets = {}
        assets["npc"] = sheet.imageAt((0, 6*16, 16, 16), scale=3)
        assets ["player"] = image.load(RESOURCES + "characters/medievalUnit_01.png")

        return assets