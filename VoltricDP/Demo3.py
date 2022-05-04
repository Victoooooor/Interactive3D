import sys

import cv2
import numpy as np

from .DemoBase import DemoBase


class Demo3(DemoBase):
    head = -1
    tail = 0
    b_len = 80
    lag_buff = [None] * b_len

    def get_slices(self, locs):
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
            print(self.tail, self.head, self.b_len, file= sys.stderr)

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

        r2 = self.c_height//2

        depth = depth * self.c_width // self.tran.width

        depth = max(depth, 0)
        depth = min(depth, self.c_width)

        center = (depth,  self.c_height * 2 // 3)

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
