import cv2
import numpy as np


from VoltricDP.Preprocess import ColorMask



class DemoBase:

    def __init__(self, color, get_frame, trans_func,
                 noise=(50, 50), turd=(5, 5), coeff=10,
                 window_name='window'):
        self.color = color
        self.hsvGreen = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)
        self.lower = self.hsvGreen[0][0][0] - 20, 95, 95
        self.upper = self.hsvGreen[0][0][0] + 20, 255, 255

        self.CM = ColorMask(self.lower, self.upper, kernel_noise=noise, kernel_turd=turd)

        self.window = window_name

        self.tran = trans_func
        self.slice_co = self.tran.width // 10

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

        self.canvas = None

    def load_canvas(self, canvas):
        self.canvas = canvas.copy()
        self.c_height = canvas.shape[0]
        self.c_width = canvas.shape[1]


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

    def get_slices(self, locs):
        pass
