import pygame as pg
from config.Settings import *
from physics.Math import euclidean, clamp


class Component:
    def __init__(self, parent, args):
        self.parent = parent
        self.args = args

    def init(self):
        pass

    def action(self):
        pass

    def update(self):
        pass

    def interact(self):
        pass

    def draw(self):
        pass

    def collisionDetected(self, object, colType=None):
        pass

    def checkArgs(self, key, alternative=None):
        if key in self.args.keys():
            return self.args[key]
        elif alternative:
            return alternative
        else:
            return None


class Consumable(Component):
    def __init__(self, parent, args):
        super().__init__(parent, args)

    def collisionDetected(self, object, colType=None):
        # print(object.name)
        if object.name == "player" and colType is "box":
            self.parent.game.level.scene.removeEntity(self.parent, self.parent.id)


class Interactable(Component):
    def __init__(self, parent, args):
        super().__init__(parent, args)
        self.fontSize = self.checkArgs("fontSize", 50)
        self.font = self.checkArgs("font", GAME_FONT)
        self.gameFont = pg.font.SysFont(self.font, self.fontSize)
        self.text = self.checkArgs("text", "text")
        self.label = self.gameFont.render(self.text, True, WHITE)

    def collisionDetected(self, object, colType=None):
        if object.name == "player" and colType is "circle":
            x = self.parent.x + self.parent.rect.width/2 - self.label.get_rect().width/2
            self.parent.game.renderer.addToQueue(self.label, (x, self.parent.y - self.fontSize))
            for e in self.parent.game.events:
                if e == INTERACT_KEY:
                    for k, c in self.parent.components.items():
                        c.interact()


class Animated(Component):
    def __init__(self, parent, args):
        super().__init__(parent, args)
        self.images = self.checkArgs("images")
        self.time = self.checkArgs("time")
        self.deltaTime = self.time/len(self.images)
        self.currentFrame = 0
        self.currentTime = 0
        # print(self.deltaTime)

    def update(self):
        self.animate()

    def animate(self):
        # print(str(self.currentTime) + " " + str(self.currentFrame))
        if self.currentTime >= (self.currentFrame+1)*self.deltaTime:
            self.currentFrame += 1
            self.parent.changeImage(self.images[self.currentFrame])
            self.currentTime += self.parent.game.dt
        else:
            self.currentTime += self.parent.game.dt

        if self.currentTime > self.time:
            self.currentFrame = 0
            self.currentTime = 0
            self.parent.changeImage(self.images[self.currentFrame])


class SoundEffect(Component):
    def __init__(self, parent, args):
        super().__init__(parent, args)
        file = self.checkArgs("sound")
        if file is not None:
            self.sound = self.parent.game.sounds[file]

        self.play = self.checkArgs("play")
        self.time = self.checkArgs("time")
        if self.time == "length":
            self.time = pg.mixer.Sound.get_length(self.sound)

        self.currentTime = 0
        self.dt = self.parent.game.dt
        self.maxVolume = self.checkArgs("volume")
        if self.maxVolume:
            pg.mixer.Sound.set_volume(self.sound, self.maxVolume)
        self.channel = None
        self.player = self.parent.game.player
        self.distance = self.checkArgs("distance", 300)

    def update(self):
        if self.player.name != "player":
            self.player = self.parent.game.player

        d = euclidean(self.parent.getPosition(), self.player.getPosition())
        v = clamp(((self.distance - d)/self.distance), 0, self.maxVolume)
        self.setVolume(v)
        print(self.parent.getPosition(), self.player.name)
        print(self.distance, d)
        print("v:", v)
        if self.channel:
            print("c: ", self.channel.get_volume())

        if self.play:
            if self.currentTime == 0:
                print("Playing sound " + self.parent.name)
                self.playSound()
                self.currentTime += self.dt
            elif self.currentTime > self.time:
                self.currentTime = 0
            else:
                self.currentTime += self.dt

    def playSound(self):
        self.channel = pg.mixer.Sound.play(self.sound)

    def playSoundOnRepeat(self):
        if self.currentTime == 0:
            self.channel = pg.mixer.Sound.play(self.sound)
            self.currentTime += self.dt
        elif self.currentTime > self.time:
            self.currentTime = 0
        else:
            self.currentTime += self.dt

    def setVolume(self, v):
        if self.channel:
            self.channel.set_volume(v)


class MusicComponent(Component):
    def __init__(self, parent, args):
        super().__init__(parent, args)
        file = self.checkArgs("sound")
        if file is not None:
            self.sound = self.parent.game.sounds[file]

        self.volume = self.checkArgs("volume")
        if self.volume:
            pg.mixer.Sound.set_volume(self.sound, self.volume)

        self.channel = None

    def playSound(self):
        self.channel = pg.mixer.Sound.play(self.sound)

    def setVolume(self, v):
        if self.channel:
            self.channel.set_volume(v)


class SceneChange(Component):
    def __init__(self, parent, args):
        super().__init__(parent, args)
        self.target = self.checkArgs("scene")
        self.tilemap = self.checkArgs("map")

    def collisionDetected(self, object, colType=None):
        if object.name == "player" and colType is "box":
            self.parent.game.setLevel(self.target, self.tilemap)

