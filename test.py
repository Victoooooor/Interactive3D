import cv2
import numpy as np

from VoltricDP.Preprocess import ColorMask
from VoltricDP.Transform import TransformPos


class Demo1:

    def __init__(self, color, get_frame, trans_func,
                 noise=(50, 50), turd=(5, 5), coeff=10,
                 window_name='window'):
        self.color = color
        self.hsvGreen = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)
        self.lower = self.hsvGreen[0][0][0] - 20, 63, 63
        self.upper = self.hsvGreen[0][0][0] + 20, 255, 255

        self.CM = ColorMask(self.lower, self.upper, kernel_noise=noise, kernel_turd=turd)

        self.window = window_name

        self.tran = trans_func

        self.get_frame = get_frame
        self.sample = self.get_frame()
        self.sample = np.zeros_like(self.sample)

        self.height = self.sample.shape[0]
        self.width = self.sample.shape[1]

        self.cols = self.width // coeff  # Horizontal length

        self.horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (self.cols, 1))

        self.background = cv2.cvtColor(self.sample, cv2.COLOR_BGR2GRAY)
        self.background = np.full_like(self.background, 255)

        self.sample = cv2.line(self.sample, (0, self.height - 11), (self.width - 1, self.height - 11),
                               color=[128, 0, 128], thickness=20)

    def get_image(self, frame, mask):
        if frame is None:
            frame = self.get_frame()

        # backup = frame.copy()
        if mask is None:
            mask = self.CM.get_mask(frame)

        res = cv2.bitwise_and(self.background, self.background, mask=mask)

        cols = res.shape[1] // 10  # Horizontal length

        horizontal = cv2.erode(res, self.horizontalStructure)
        horizontal = cv2.dilate(horizontal, self.horizontalStructure)

        return horizontal

    def get_loc(self, frame=None, mask=None):
        frame = self.get_image(frame, mask)

        contours, centers = self.CM.get_cc(frame)

        centers = np.float32(np.array(centers))
        centers = np.expand_dims(centers, axis=1)
        # pts = np.float32(np.array([[[1920, 1280]]]))
        # canvas = sample.copy()

        centers = self.tran.get_top_pos(centers)
        return centers


# Webcam/Any Input Feed
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

d1 = Demo1(color, get_frame, tp)

if __name__ == "__main__":

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # cv2.moveWindow('window', 1980, 0)

    while True:

        cv2.waitKey(1000 // 30)

        canvas = d1.sample.copy()

        points = d1.get_loc()
        for p in points:
            canvas = cv2.circle(canvas, p, radius=30, color=(0, 0, 255), thickness=-1)

        # cv2.drawContours(canvas,contours, -1, (0, 255, 0), 10)
        else:
            # print('empty')
            None

        cv2.imshow('window', canvas)
