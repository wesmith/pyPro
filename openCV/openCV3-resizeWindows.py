import cv2
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0

# gstreamer command line for pi camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam1 = cv2.VideoCapture(camSet)

# the following is for the webcam
cam2 = cv2.VideoCapture(1)
cam2.set(cv2.CAP_PROP_FRAME_WIDTH,  dispW)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()
    cv2.imshow('piCam', frame1)
    cv2.moveWindow('piCam', 700, 0)

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    frameSmall1 = cv2.resize(frame1, (320, 240))
    graySmall1  = cv2.resize(gray1,  (320, 240))
    frameSmall2 = cv2.resize(frame2, (320, 240))
    graySmall2  = cv2.resize(gray2,  (320, 240))

    cv2.moveWindow('piCamSmallBW', 0, 265)
    cv2.moveWindow('piCamSmall', 0, 0)
    cv2.imshow('piCamSmallBW', graySmall1)
    cv2.imshow('piCamSmall', frameSmall1)

    cv2.moveWindow('WebCamSmallBW', 385, 265)
    cv2.moveWindow('WebCamSmall', 385, 0)
    cv2.imshow('WebCamSmallBW', graySmall2)
    cv2.imshow('WebCamSmall', frameSmall2)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

