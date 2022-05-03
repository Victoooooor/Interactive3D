import os

import cv2
import numpy as np

from VoltricDP.Display import Display

width = 1920
height = 1080

slices_path = './slices'
cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

if __name__ == '__main__':
    DD = Display()
    DD.load(slices_path)

    src = cv2.imread('test.jpg')
    src2 = cv2.imread('test2.jpg')

    out = DD.produce_full([src, src2])
    print(DD.approx)
    cv2.imshow('window', out)
    cv2.waitKey()

