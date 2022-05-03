import cv2
width = 1920
height = 1080

fname  = 'test.jpg'
pic = cv2.imread(fname)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# cv2.imshow('window',pic)

alpha = 3 # Contrast control (1.0-3.0)
beta = -100 # Brightness control (0-100)


while True:
    cv2.waitKey(1000//10)
    frame = cam.read()[1]
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    cv2.imshow('window', frame)
