import cv2

from VoltricDP import V2D


def draw(frame, mask, centers):
    segmented_img = cv2.bitwise_and(frame, frame, mask=mask)
    # cv2.drawContours(segmented_img, contours, -1, (0, 0, 255), 3)
    for c, r in centers:
        segmented_img = cv2.circle(segmented_img, c, r, (255, 255, 255), 2)
    return segmented_img


class CamPos(object):

    def __init__(self, handle, get_frame, viz=False):
        self.get_frame = get_frame
        self.handle = handle
        frame = self.get_frame()
        self.h, self.w, _ = frame.shape
        self.visualize = viz

    def get_pos(self):
        frame = self.get_frame()
        mask = self.handle.get_mask(frame)
        contours, centers = self.handle.get_cc(mask)
        circles = self.handle.get_circle(contours)
        if self.visualize:
            final = draw(frame, None, circles)
            cv2.imshow('get_pos', final)
        if len(circles) > 0:
            x, y = circles[0][0]
            radius = circles[0][1]

            return V2D(x / self.w, y / self.h), radius
        else:
            return None

