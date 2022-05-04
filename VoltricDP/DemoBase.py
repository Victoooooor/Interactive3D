import cv2
import numpy as np


from VoltricDP.Preprocess import ColorMask



class DemoBase:

    def __init__(self, color, get_frame, trans_func,
                 noise=(3, 3), turd=(10, 10), coeff=10,
                 window_name='window'):
        self.color = color
        self.hsvGreen = cv2.cvtColor(color, cv2.COLOR_RGB2HSV)
        self.lower = self.hsvGreen[0][0][0] - 40, 31, 31
        self.upper = self.hsvGreen[0][0][0] + 40, 255, 255

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


    def seg_frame(self):
        frame = self.get_frame()
        frame[: 550, :, :] = 0
        frame[680:, :, :] = 0   #660
        frame[:,:256,:] = 0
        frame[:,850:, :] = 0
        return frame

    def bright_mask(self, frame):
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(grey, 111, 255, cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, (7, 7))  # noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (10, 10))
        return mask

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

        mask = self.get_image(frame, mask)

        pts = np.argwhere(mask > 0)
        y= np.average(pts[:,0]).astype(np.int)
        x = np.average(pts[:,1]).astype(np.int)

        # t_sum = np.sum(mask)
        # if t_sum == 0:
        #     return []
        # x_sum = np.sum(mask, axis = 1)
        #
        # x_sum = x_sum * np.arange(len(x_sum))
        #
        # x_sum = np.sum(x_sum) // t_sum
        #
        # y_sum = np.sum(mask, axis = 0)
        #
        # y_sum = y_sum * np.arange(len(y_sum))
        #
        # y_sum = np.sum(y_sum) // t_sum
        # #
        # # contours, centers = self.CM.get_cc(frame)
        # # print(centers)
        if x< 0 or y < 0:
            return []
        centers = [(x, y)]
        # print(centers)
        # print(centers)
        centers = np.float32(np.array(centers))
        # return []
        centers = np.expand_dims(centers, axis=1)

        # print(centers)
        # pts = np.float32(np.array([[[1920, 1280]]]))
        # canvas = sample.copy()
        centers = self.tran.get_top_pos(centers)
        return centers

    def get_slices(self, locs):
        pass
