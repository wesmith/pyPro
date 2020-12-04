import cv2
print(cv2.__version__)
scale = 1
dispW = 320 * scale
dispH = 240 * scale
flip = 0

# gstreamer command line for pi camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)

# the following is for the webcam
#cam = cv2.VideoCapture(1)
while True:
    ret, frame = cam.read()
    cv2.imshow('piCam', frame)
    cv2.moveWindow('piCam', 0, 0)
    cv2.imshow('piCam2', frame)
    cv2.moveWindow('piCam2', dispW + 50, 0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    cv2.moveWindow('gray', 0, dispH + 50)
    cv2.imshow('gray2', gray)
    cv2.moveWindow('gray2', dispW + 50, dispH + 50)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

