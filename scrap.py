import cv2
import numpy as np

src = np.float32([[0, 1280], [1920, 1280], [1920, 0], [0, 0]])
dst = np.float32([[0, 600], [400, 600], [400, 0], [0, 0]])
perspective_transform = cv2.getPerspectiveTransform(src, dst)
pts = np.float32(np.array([[[1920, 1280]]]))
warped_pt = cv2.perspectiveTransform(pts, perspective_transform)[0]
print ("warped_pt = ", warped_pt)