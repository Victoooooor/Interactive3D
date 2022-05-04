import cv2
import numpy as np

from .DemoBase import DemoBase


class Demo2(DemoBase):

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
            slit = np.expand_dims(slit, axis = 1)
            curr = np.repeat(slit, self.c_width, axis = 1)
            slices.append(curr.copy())

        return slices
