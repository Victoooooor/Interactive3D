import cv2
import numpy as np

class ColorMask:
    def __init__(self,
                 lower=[15, 127, 127],
                 upper=[36, 255, 255],
                 kernel_noise=(20, 20),
                 kernel_turd=(15, 15)):
        self.lower = np.array(lower)
        self.upper = np.array(upper)
        self.kernel_noise = np.ones(kernel_noise, np.uint8)
        self.kernel_turd = np.ones(kernel_turd, np.uint8)

    def get_mask(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.lower, self.upper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel_noise)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel_turd)

        return mask

    def get_cc(self, mask):
        centers = []
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            center = cv2.moments(contour)
            cX = round(center["m10"] / center["m00"])
            cY = round(center["m01"] / center["m00"])
            centers.append((cX, cY))
        return contours, centers

    def get_rec(self, contours):
        boxes = []
        for c in contours:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            boxes.append(box)
        return boxes

    def get_circle(self, contours):
        circles = []
        for c in contours:
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            circles.append((center, radius))
        return circles
