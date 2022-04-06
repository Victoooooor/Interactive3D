# Template for initializing pygame

import pygame as game


class App:

    running = True  # keep the application running
    screen = None  # window handler pointer
    flags = game.HWSURFACE | game.DOUBLEBUF  # hardware acceleration and double buffering

    def __init__(self, t="Volumetric Display", x=550, y=400, f=30):
        self.title = t
        self.size = (x, y)
        self.center = (x // 2, y // 2)
        self.framerate = f
        self.init()

    def run(self):
        game.init()
        game.display.set_caption(self.title)
        self.screen = game.display.set_mode(self.size, self.flags)
        self.running = True

        while self.running:
            for event in game.event.get():
                self.handler(event)
            self.update()
            self.render()
            game.time.delay(round(1000 / self.framerate))
        self.clean()

    def handler(self, event):
        if event.type == game.QUIT:
            self.running = False

    def clean(self):
        game.quit()

    def exit(self):
        self.running = False

    def init(self):
        pass

    def update(self):
        pass

    def render(self):
        pass
