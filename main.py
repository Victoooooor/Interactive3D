import cv2
import numpy as np
import pygame as game

from VoltricDP.V2D import V2D
from VoltricDP.Preprocess import ColorMask
from VoltricDP.SoftSquare import SoftSquare
from VoltricDP.CamHandler import CamPos


if __name__ == "__main__":
    # Webcam & Canvas Dim
    width = 1920
    height = 1080

    # Define Color range in HSV
    color = np.uint8([[[128, 0, 128]]])  # in rgb
    hsvGreen = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)
    lower = hsvGreen[0][0][0] - 20, 127, 127
    upper = hsvGreen[0][0][0] + 20, 255, 255

    noise = (50, 50)
    turd = (20, 20)

    # Webcam/Any Input Feed
    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Function for frame
    get_frame = lambda: cv2.flip(vid.read()[1], 1)

    # Mouse Position
    MP = lambda: (V2D(game.mouse.get_pos()[0], game.mouse.get_pos()[1]), 100)

    # Initialize Preprocessor for Input
    CM = ColorMask(lower, upper, kernel_noise=noise, kernel_turd=turd)
    CP = CamPos(CM, get_frame)

    # Initialize SoftBody Structure
    m = 1.0
    f = 0.8
    b = 0.1

    # Use Video
    main = SoftSquare(CP.get_pos, (m, f, b), "Main", width, height, 30, fill=True)

    # Use mouse
    # main = SoftSquare(MP, (m, f, b), "Main", width, height, 30, fill=False)

    # main.load_alpha('./mask1920x1080.png')
    main.load_alpha('./A9em5.png')
    main.run()

    # while cv2.waitKey(1) & 0xFF != ord('q'):
    #     CP.get_pos(draw=True)

    vid.release()
    cv2.destroyAllWindows()
