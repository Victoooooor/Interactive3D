import pygame as game
import cv2

class SoftBase:
    # Template functions
    def _init(self):
        pass

    def _update(self):
        pass

    def _render(self):
        pass

    def __init__(self, title="Main", x=1280, y=720, f=30):
        self.alpha = None
        self.running = None
        self.screen = None
        self.background = None
        self.flags = game.HWSURFACE | game.DOUBLEBUF  # | game.OPENGL

        self.title = title
        self.size = (x, y)
        self.center = (x // 2, y // 2)
        self.framerate = f

        self._init()

        game.init()
        game.display.set_caption(self.title)
        self.screen = game.display.set_mode(self.size, self.flags)
        self.background = game.Surface(self.size, game.SRCALPHA)
        self.running = True

    def _handler(self, event):
        if event.type == game.QUIT:
            self.running = False

    def load_alpha(self, alpha_file):

        im = cv2.imread(alpha_file, cv2.IMREAD_UNCHANGED)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        c = im.shape[2]
        if c == 4:
            self.alpha = game.image.frombuffer(im, im.shape[1::-1], "RGBA").convert_alpha()
        elif c == 3:
            self.alpha = game.image.frombuffer(im, im.shape[1::-1], "RGB").convert_alpha()
        else:
            print("unsupported file format")
            exit(-1)
        self.alpha = game.transform.scale(self.alpha, self.size)

    def run(self):

        while self.running:
            for event in game.event.get():
                self._handler(event)
            self._update()
            self._render()
            game.time.wait(round(1000 / self.framerate))

        game.quit()



