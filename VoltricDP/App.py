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
        self.Initialize()

    def Run(self):
        game.init()
        game.display.set_caption(self.title)
        self.screen = game.display.set_mode(self.size, self.flags)
        self.running = True

        while self.running:
            for event in game.event.get():
                self.HandleEvent(event)
            self.Update()
            self.Render()
            game.time.delay(round(1000 / self.framerate))
        self.CleanUp()

    def HandleEvent(self, event):
        if event.type == game.QUIT:
            self.running = False

    def CleanUp(self):
        game.quit()

    def Exit(self):
        self.running = False

    def Initialize(self):
        pass

    def Update(self):
        pass

    def Render(self):
        pass
