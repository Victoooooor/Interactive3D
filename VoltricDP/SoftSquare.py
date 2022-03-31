from . import *


class SoftSquare(App):

    def __init__(self, input_func, t='Application', x=960, y=720, f=30, c=[(255, 0, 0), (255, 255, 0), (255, 0, 255)],
                 res=16, fill=True):
        self.world = World(Vector(x / 1.0, y / 1.0), Vector(0, 2), 2)
        self.objpos = Vector()
        self.previous = Vector()
        self.strength = 3.0
        self.radius = 30
        self.step = res
        self.fill = fill
        self.color = c

        self.color[1] = tuple(map(lambda i, j: (i - j) // (self.step - 1), self.color[1], self.color[0]))
        self.color[2] = tuple(map(lambda i, j: (i - j) // (self.step - 1), self.color[2], self.color[0]))

        self.minX = x // 5
        self.maxX = self.minX * 4
        self.minY = y // 6
        self.maxY = y * 3 // 4

        self.get_pose = input_func
        # Initialize App
        super().__init__(t=t, x=x, y=y, f=f)

    #
    def Initialize(self):
        #
        squareshape = self.world.AddComposite()

        nodes = list()
        const = list()

        size = Vector((self.maxX - self.minX) / self.step, (self.maxY - self.minY) / self.step)

        # generate particles in a grid
        for y in range(self.step):
            nodes.append(list())
            for x in range(self.step):
                nodes[y].append(self.world.AddParticle(self.minX + x * size.x, self.minY + y * size.y))
                if not y:
                    nodes[y][x].material.mass = 0.0
                # elif y == self.step - 1:
                #     nodes[y][x].ApplyForce(Vector(50.0, random.random() * -500.0))

        # add horizontal constraints
        for y in range(self.step):
            for x in range(1, self.step):
                const.append(self.world.AddConstraint(nodes[y][x - 1], nodes[y][x], 1.0))

        # add vertical constraints
        for y in range(1, self.step):
            for x in range(self.step):
                const.append(self.world.AddConstraint(nodes[y - 1][x], nodes[y][x], 1.0))

        squareshape.AddParticles(nodes)
        squareshape.AddConstraints(const)

    def Update(self):
        #
        self.objpos = self.get_pose()

        if self.objpos is None:
            self.previous = Vector()
        else:
            self.objpos.scale(self.world.size)
            force = (self.objpos - self.previous) * self.strength
            for particle in self.world.particles:
                if self.objpos.distance(particle.position) < self.radius:
                    particle.ApplyForce(force)
            # if game.mouse.get_pressed()[0]:
            self.previous = self.objpos
        #
        if game.key.get_pressed()[game.K_ESCAPE]:
            self.Exit()
        self.world.Simulate()

    #
    def Render(self):
        #
        self.screen.fill((24, 24, 24))

        if self.fill:  # Display Colored Block

            for i in range(self.step - 1):
                for j in range(self.step - 1):
                    points = [i * self.step + j,
                              i * self.step + j + 1,
                              (i + 1) * self.step + j + 1,
                              (i + 1) * self.step + j]
                    points = [self.world.particles[p].position.to_tuple() for p in points]
                    cur_color = tuple(
                        map(lambda a, b, c: a + i * b + j * c, self.color[0], self.color[1], self.color[2]))
                    game.draw.polygon(self.screen, cur_color, points)

        else:  # Display Skeleton

            for i in range(self.step):
                for j in range(self.step):
                    cur_color = tuple(
                        map(lambda a, b, c: a + i * b + j * c, self.color[0], self.color[1], self.color[2]))
                    points = [i * self.step + j,
                           i * self.step + j + 1,
                           (i + 1) * self.step + j]
                    points = [self.world.particles[p].position.to_tuple() if p < self.step * self.step else None for p in points]
                    if i < self.step - 1:
                        game.draw.line(self.screen, cur_color, points[0], points[2], 2)
                    if j < self.step - 1:
                        game.draw.line(self.screen, cur_color, points[0], points[1], 2)


        game.display.update()
