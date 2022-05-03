import os

import cv2
import numpy as np

class Display(object):

    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.slices = []
        self.approx = []
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.corners = np.array([[0, 0],
                                 [0, height - 1],
                                 [width - 1, 0],
                                 [width - 1, height - 1]])

    # load all slices in order left to right
    def load_slice(self, slice):

        slice = cv2.cvtColor(slice, cv2.COLOR_BGR2GRAY)
        ret, im = cv2.threshold(slice, 100, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0]
        app = cv2.approxPolyDP(contours, 10, True)
        app = [x[0] for x in app]
        app = np.array(sorted(app, key=lambda x: tuple(x)))
        h, _ = cv2.findHomography(self.corners, app)

        self.slices.append(h)
        app[[2, 3]] = app[[3, 2]]
        self.approx.append(app)

    # wrapper to load all slices
    def load(self, path):
        for i in range(10):
            full_path = os.path.join(path, str(i+1)+'-01.png')
            try:
                slice = cv2.imread(full_path)
            except:
                print('Load fill access error')
                exit(-1)
            self.load_slice(slice)

    # provide all slices in list, use None if blank
    def produce_full(self, frames):
        total = self.canvas.copy()
        for i, f in enumerate(frames):
            if f is None:
                continue
            temp_mask = np.zeros_like(total)
            cv2.fillConvexPoly(temp_mask, self.approx[i], (255,) * 3)
            temp_mask = cv2.bitwise_not(temp_mask)
            total = cv2.bitwise_and(total, temp_mask)

            out = cv2.warpPerspective(f, self.slices[i], (self.canvas.shape[1], self.canvas.shape[0]))

            total = cv2.bitwise_or(out, total)

        return total