import cv2
import numpy as np


class TransformPos(object):

    def __init__(self, width=1000, height=1000):
        self.h = None  # perspective matrix
        self.width = width
        self.height = height

        self.corners = np.float32([[0, 0], [0, height - 1], [width - 1, 0], [width - 1, height - 1]])

    def def_field(self, field_corners):
        self.h = cv2.getPerspectiveTransform(field_corners, self.corners)

    def get_top_pos(self, points):
        if len(points) == 0:
            return []

        abs_axis = cv2.perspectiveTransform(points, self.h)
        transformed = [tuple(pp[0].astype(int)) for pp in abs_axis]

        return transformed
