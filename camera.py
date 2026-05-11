import pygame
from abc import ABC
from settings import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT

vec = pygame.math.Vector2


#-----------------------------------------------------------------------------------------------
class Camera:
    def __init__(self, player, width, height, map_width, map_height):
        self.player = player

        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)

        self.DISPLAY_W = width
        self.DISPLAY_H = height

        self.map_width = map_width
        self.map_height = map_height

        
        self.CONST = vec(
            -self.DISPLAY_W / 2 + player.rect.w / 2,
            -self.DISPLAY_H / 2 + player.rect.h / 2
        )

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()

#-----------------------------------------------------------------------------------------------
class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    def scroll(self):
        pass

#-----------------------------------------------------------------------------------------------
class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        target_x = self.player.rect.x + self.camera.CONST.x
        target_y = self.player.rect.y + self.camera.CONST.y

        self.camera.offset_float.x += (target_x - self.camera.offset_float.x) * 0.08
        self.camera.offset_float.y += (target_y - self.camera.offset_float.y) * 0.1

        self.camera.offset.x = int(self.camera.offset_float.x)
        self.camera.offset.y = int(self.camera.offset_float.y)

#-----------------------------------------------------------------------------------------------
class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        target_x = self.player.rect.x + self.camera.CONST.x
        target_y = self.player.rect.y + self.camera.CONST.y

        self.camera.offset_float.x += (target_x - self.camera.offset_float.x) * 0.08
        self.camera.offset_float.y += (target_y - self.camera.offset_float.y) * 0.08

        self.camera.offset.x = int(self.camera.offset_float.x)
        self.camera.offset.y = int(self.camera.offset_float.y)

        # Clamp camera to map bounds
        self.camera.offset.x = max(0, self.camera.offset.x)
        self.camera.offset.y = max(0, self.camera.offset.y)
        
        self.camera.offset.x = min(self.camera.offset.x, self.camera.map_width - self.camera.DISPLAY_W)
        self.camera.offset.y = min(self.camera.offset.y, self.camera.map_height - self.camera.DISPLAY_H)
