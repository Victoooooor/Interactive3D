import random

import cv2
import numpy as np

from VoltricDP import *
from VoltricDP.Preprocess import ColorMask
from VoltricDP.SoftSquare import SoftSquare
from VoltricDP.CamHandler import CamPos


if __name__ == "__main__":

    # Webcam & Canvas Dim
    width = 1280
    height = 720

    # Define Color range in HSV
    yellow = np.uint8([[[255,255,0]]])  # in rgb
    hsvGreen = cv2.cvtColor(yellow, cv2.COLOR_RGB2HSV)
    lower = hsvGreen[0][0][0] - 20, 111, 111
    upper = hsvGreen[0][0][0] + 20, 255, 255

    noise = (50,50)
    turd = (20,20)

    # Webcam/Any Input Feed
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Function for frame
    get_frame = lambda: cv2.flip(vid.read()[1],1)

    # Mouse Position
    # MP = lambda: Vector(game.mouse.get_pos()[0], game.mouse.get_pos()[1])

    # Initialize Preprocessor for Input
    CM = ColorMask(lower, upper, kernel_noise= noise, kernel_turd= turd)
    CP = CamPos(CM,get_frame)

    # Initialize SoftBody Structure

    app = SoftSquare(CP.get_pos, "Main", width, height, 30, fill = False)
    app.Run()

    # while cv2.waitKey(1) & 0xFF != ord('q'):
    #     CP.get_pos(draw=True)

    vid.release()
    cv2.destroyAllWindows()
