import cv2
import numpy as np

from .DemoBase import DemoBase


class Demo(DemoBase):
    head = -1
    tail = 0
    b_len = 80
    lag_buff = [None] * b_len

    def get_slices_1(self, locs):
        length = len(locs)

        try:
            if length != 0:

                total = [0, 0]
                for i in locs:
                    total[0] += i[0]
                    total[1] += i[1]

                total = [x // length for x in total]
                self.lag_buff[self.tail] = total
                self.tail += 1
                # print(self.tail)
            else:
                None
                # self.lag_buff[self.tail] = None
                # pass

        except IndexError:
            if self.head < 0:
                self.head = 0
            self.tail %= self.b_len
            print(self.tail, self.head, self.b_len, file=sys.stderr)

        if self.head < 0:
            return []

        x = self.lag_buff[self.head][0]
        depth = self.tran.height - self.lag_buff[self.head][1] - 1

        self.head += 1
        self.head %= self.b_len

        if self.head == self.tail:  # wrap around
            self.tail = 0
            self.head = -1

        x_slice = x // self.slice_co

        slices = []

        radius = self.c_width // 8

        r2 = self.c_height // 2

        depth = depth * self.c_width // self.tran.width

        depth = max(depth, 0)
        depth = min(depth, self.c_width)

        center = (depth, self.c_height * 2 // 3)

        axslen = (radius, r2)
        angle = 180

        startAngle = 0

        endAngle = 360

        # Red color in BGR
        color = (255, 255, 255)

        # Line thickness of 5 px
        thickness = -1

        # Using cv2.ellipse() method
        # Draw a ellipse with red line borders of thickness of 5 px

        # curr = self.canvas.copy()

        # curr = cv2.ellipse(curr, center, axslen,
        #                    angle, startAngle, endAngle, color, thickness)

        for i in range(10):
            curr = self.canvas.copy()

            if x_slice - 1 <= i <= x_slice + 1:
                dis = abs(x - i * self.slice_co)
                cur_axslen = tuple([x - dis for x in axslen])
                cur_color = tuple([int(x - dis) for x in color])
                # print(cur_color)
                curr = cv2.ellipse(curr, center, cur_axslen,
                                   angle, startAngle, endAngle, cur_color, thickness)

                slices.append(curr)
            else:
                slices.append(None)

        return slices

    def get_slices_2(self, locs):
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

        depth = self.tran.height - total[1] - 1
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

    def get_slices_3(self, locs):
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

        depth = self.tran.height - total[1] - 1
        # slices = []
        flat = self.canvas.copy()

        radius = self.c_width * 2 // 11
        r2 = radius * 2 // 3
        x = x * self.c_width // self.tran.width

        center = (x, r2 + 20)

        axslen = (radius, r2)
        angle = 180

        startAngle = 0

        endAngle = 180

        # Red color in BGR
        color = (255, 255, 255)

        # Line thickness of 5 px
        thickness = 20

        # Using cv2.ellipse() method
        # Draw a ellipse with red line borders of thickness of 5 px
        flat = cv2.ellipse(flat, center, axslen,
                           angle, startAngle, endAngle, color, thickness)
        flat = cv2.line(flat, (0, center[1]), (x - radius, center[1]),
                        color=color, thickness=thickness)
        flat = cv2.line(flat, (x + radius, center[1]), (x * self.c_width, center[1]),
                        color=color, thickness=thickness)

        slices = []

        diff = (self.c_width - 1) // 9

        for i in range(10):
            x_cur = i * diff
            slit = flat[:, x_cur, :]
            slit = np.expand_dims(slit, axis=1)
            curr = np.repeat(slit, self.c_width, axis=1)
            slices.append(curr.copy())

        return slices