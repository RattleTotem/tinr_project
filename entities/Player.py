import pygame as pg

from config.Settings import *
from entities.Entity import Entity


class Player(Entity):
    def __init__(self, position, name, image, game, entityID, scale=(1, 1), rect=None):
        Entity.__init__(self, position, name, image, game, entityID, scale=scale, rect=rect)
        self.vx, self.vy = 0, 0
        self.moving = False
        self.sound = None
        self.label = None
        self.health = 10
        self.speed = PLAYER_SPEED

    def init(self):
        self.sound = self.components["SoundEffect"]
        self.label = self.game.gui.getElement(name="Position")
        # self.label = self.game.gui.c

    def damaged(self, damage):
        self.health -= damage

    def update(self):
        # print(self.health)
        self.checkSprint()
        if self.health <= 0:
            self.game.gameOver()
        self.move()
        for i, c in self.components.items():
            # c.action()
            pass
        if self.sound:
            self.playSound()

        # print(self.label.name)
        if self.label:
            self.label.setText(self.getPosition())

    def move(self):
        velocity = pg.Vector2((0, 0))
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            velocity.x = -1
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            velocity.x = 1
        if keys[pg.K_UP] or keys[pg.K_w]:
            velocity.y = -1
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            velocity.y = 1

        if velocity.length() != 0:
            velocity = velocity.normalize()

        self.x += velocity.x * self.speed * self.game.dt
        self.y += velocity.y * self.speed * self.game.dt

        self.rect.x = self.x
        self.rect.y = self.y

        if velocity.x != 0 or velocity.y != 0:
            self.moving = True
        else:
            self.moving = False

        # print(velocity)

    def playSound(self):
        if self.moving:
            # print("playing")
            self.sound.playSoundOnRepeat()

    def checkSprint(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            self.speed = PLAYER_SPEED * 2
        else:
            self.speed = PLAYER_SPEED
