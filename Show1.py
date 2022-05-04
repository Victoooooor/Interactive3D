import cv2
import numpy as np

from VoltricDP.Transform import TransformPos
from VoltricDP.Display import Display
from VoltricDP.Demo1 import Demo1

# Webcam/Any Input Feed

slices_path = './slices'

width = 1280
height = 720

top_dim = 1000

color = np.uint8([[[128, 0, 128]]])
vid = cv2.VideoCapture(1)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Function for frame
get_frame = lambda: cv2.flip(vid.read()[1], 1)

field = np.float32([[427, 555], [410, 656], [784, 557], [788, 645]])
tp = TransformPos(1000, 1000)
tp.def_field(field)
field = np.expand_dims(field, axis=1)

print(tp.get_top_pos(field))

d1 = Demo1(color, get_frame, tp, coeff = 60)

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
        frame = d1.seg_frame()

        # mask = d1.CM.get_mask(frame)
        mask = d1.bright_mask(frame)
        # bi = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        # cv2.THRESH_BINARY, 199, 5)
        points = d1.get_loc(frame, mask)  # x, y
        # print(points)
        slices = d1.get_slices(points)
        # print(points)
        out = DD.produce_full(slices)

        cv2.imshow('window', out)
        cv2.imshow('frame', frame)


        # cv2.imshow('grey', grey)
        cv2.imshow('binary', mask)
        # cv2.imshow('mask', mask)
        cv2.imshow('hrizontal', d1.get_image(frame, mask))
