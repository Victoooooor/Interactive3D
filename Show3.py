import cv2
import numpy as np

from VoltricDP.Transform import TransformPos
from VoltricDP.Display import Display
from VoltricDP.Demo3 import Demo3

# Webcam/Any Input Feed

slices_path = './slices'

width = 1920
height = 1080

top_dim = 1000

color = np.uint8([[[128, 0, 128]]])
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Function for frame
get_frame = lambda: cv2.flip(vid.read()[1], 1)

field = np.float32([[300, 200], [200, height - 201], [width - 301, 200], [width - 201, height - 201]])
tp = TransformPos(1000, 1000)
tp.def_field(field)
field = np.expand_dims(field, axis=1)

print(tp.get_top_pos(field))

d1 = Demo3(color, get_frame, tp)

DD = Display()
DD.load(slices_path)

if __name__ == "__main__":

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # cv2.moveWindow('window', 1980, 0)


    d1.load_canvas(DD.canvas)

    while True:

        cv2.waitKey(1000 // 120)

        # canvas = d1.sample.copy()
        frame = d1.get_frame()

        mask = d1.CM.get_mask(frame)
        points = d1.get_loc(frame, mask)  # x, y
        slices = d1.get_slices(points)
        # print(centered)
        # for p in points:
        #     canvas = cv2.circle(canvas, p, radius=30, color=(0, 0, 255), thickness=-1)
            # print(p)
        # cv2.drawContours(canvas,contours, -1, (0, 255, 0), 10)
        # else:
        #     # print('empty')
        #     None
        out = DD.produce_full(slices)

        cv2.imshow('window', out)
        # cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask)
