import cv2
import numpy as np

from .DemoBase import DemoBase


class Demo1(DemoBase):

    def get_slices(self, locs):
        length = len(locs)

        if length == 0:
            return []

        total = [0, 0]
        for i in locs:
            total[0] += i[0]
            total[1] += i[1]

        total = [x // length for x in total]

        x = total[0]

        x_slice = x // self.slice_co

        depth = self.tran.height - total[1]
        slices = []

        for i in range(10):
            curr = self.canvas.copy()

            if i < x_slice - 1:
                x_shift = x - self.slice_co
                left = depth * self.c_width * self.slice_co * i // (x_shift * self.tran.width)
                right = self.c_width - (self.tran.width - depth) * self.c_width * self.slice_co * i // (
                            x_shift * self.tran.width)
                top = self.c_height * 50 * i // x_shift
                bottom = self.c_height - top
                shape = np.array([[left, top],
                                  [left, bottom],
                                  [right, bottom],
                                  [right, top]])
                curr = cv2.fillConvexPoly(curr, shape, (255,) * 3)
                slices.append(curr)

            elif i > x_slice + 1:
                x_shift = x + self.slice_co
                right = depth * self.c_width * self.slice_co * (9 - i) // (x_shift * self.tran.width)
                left = self.c_width - (self.tran.width - depth) * self.c_width * self.slice_co * (9 - i) // (
                            x_shift * self.tran.width)
                top = self.c_height * 50 * (9 - i) // x_shift
                bottom = self.c_height - top
                shape = np.array([[left, top],
                                  [left, bottom],
                                  [right, bottom],
                                  [right, top]])
                curr = cv2.fillConvexPoly(curr, shape, (255,) * 3)
                slices.append(curr)

            else:
                slices.append(None)

        return slices
