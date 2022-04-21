import pygame as game


class SoftBase:
    # Template functions
    def _init(self):
        pass

    def _update(self):
        pass

    def _render(self):
        pass

    def __init__(self, title="Main", x=1280, y=720, f=30):
        self.running = None
        self.screen = None
        self.flags = game.HWSURFACE | game.DOUBLEBUF  # | game.OPENGL

        self.title = title
        self.size = (x, y)
        self.center = (x // 2, y // 2)
        self.framerate = f

        self._init()

    def _handler(self, event):
        if event.type == game.QUIT:
            self.running = False

    def run(self):
        game.init()
        game.display.set_caption(self.title)
        self.screen = game.display.set_mode(self.size, self.flags)
        self.running = True

        while self.running:
            for event in game.event.get():
                self._handler(event)
            self._update()
            self._render()
            game.time.wait(round(1000 / self.framerate))

        game.quit()



