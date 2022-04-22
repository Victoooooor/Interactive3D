from . import *


class SoftSquare(SoftBase):

    def __init__(self, input_func, mat,
                 title='Soft Square', x=1280, y=720, f=30,
                 c=[(255, 0, 0), (255, 255, 0), (255, 0, 255)],
                 res=16, fill=True):

        self.world = World(V2D(x / 1.0, y / 1.0), V2D(0, 2), 2)
        self.curr = V2D()
        self.prev = V2D()

        # default m/f/b val
        self.mat = mat

        self.color = c
        self.res = res
        self.fill = fill

        self.scale = 1.5
        self.radius = 20

        self.color[1] = tuple(map(lambda i, j: (i - j) // (self.res - 1), self.color[1], self.color[0]))
        self.color[2] = tuple(map(lambda i, j: (i - j) // (self.res - 1), self.color[2], self.color[0]))

        self.minX = x // 5
        self.maxX = self.minX * 4
        self.minY = y // 6
        self.maxY = y * 3 // 4

        self.get_pose = input_func

        # Initialize Render
        super().__init__(title=title, x=x, y=y, f=f)

    #
    def _init(self):
        nodes = []
        constraints = []

        grid = V2D((self.maxX - self.minX) / self.res, (self.maxY - self.minY) / self.res)

        # node
        for y in range(self.res):
            nodes.append([])
            for x in range(self.res):
                nodes[y].append(self.world.add_node(self.minX + (x * grid.x),
                                                    self.minY + (y * grid.y),
                                                    self.mat if y else
                                                    (0.0,) + self.mat[1:]
                                                    ))

        # string
        for y in range(self.res):
            for x in range(1, self.res):
                constraints.append(self.world.add_edge(nodes[y][x - 1], nodes[y][x], 1.0))
        for y in range(1, self.res):
            for x in range(self.res):
                constraints.append(self.world.add_edge(nodes[y - 1][x], nodes[y][x], 1.0))

        obj = self.world.add_body()
        obj.add_nodes(nodes)
        obj.add_edges(constraints)

    def _update(self):
        temp = self.get_pose()

        if temp is None:
            None
        else:
            self.curr, self.radius = temp
            if self.curr.x < 1 and self.curr.y < 1:
                self.curr.scale(self.world.size)
            force = (self.curr - self.prev) * self.scale
            for node in self.world.nodes:
                dis = max(self.curr.distance(node.curr), 1)
                temp = self.radius / dis
                if temp > 1:
                    node.add_force(force)
                if temp > 2:
                    repel = (node.curr - self.curr) * temp
                    node.add_force(repel)
            self.prev = self.curr

        if game.key.get_pressed()[game.K_ESCAPE]:
            self._handler(game.QUIT)

        self.world.step()

    def _render(self):
        # background color
        self.background.fill((0, 0, 0))

        if self.fill:  # Display Colored Block

            for i in range(self.res - 1):
                for j in range(self.res - 1):
                    points = [i * self.res + j,
                              i * self.res + j + 1,
                              (i + 1) * self.res + j + 1,
                              (i + 1) * self.res + j]
                    points = [tuple(self.world.nodes[p].curr) for p in points]
                    cur_color = tuple(
                        map(lambda a, b, c: a + i * b + j * c, self.color[0], self.color[1], self.color[2]))
                    game.draw.polygon(self.background, cur_color, points)

        else:  # Display Skeleton

            for i in range(self.res):
                for j in range(self.res):
                    cur_color = tuple(
                        map(lambda a, b, c: a + i * b + j * c, self.color[0], self.color[1], self.color[2]))
                    points = [i * self.res + j,
                              i * self.res + j + 1,
                              (i + 1) * self.res + j]
                    points = [tuple(self.world.nodes[p].curr) if p < self.res * self.res else None
                              for p in points]
                    if i < self.res - 1:
                        game.draw.line(self.background, cur_color, points[0], points[2], 2)
                    if j < self.res - 1:
                        game.draw.line(self.background, cur_color, points[0], points[1], 2)

        if self.alpha is not None:
            # print("mask"
            # print(self.alpha)
            self.background.blit(self.alpha, (0, 0), None, game.BLEND_RGBA_MULT)

        self.screen.blit(self.background, (0, 0))

        game.display.flip()
