import cv2
print(cv2.__version__)
dispW = 320 * 2
dispH = 240 * 2
flip = 0
# gstreamer command line
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
PiCam  = cv2.VideoCapture(camSet)
#WebCam = cv2.VideoCapture(1)
while True:
    ret,  frame  = PiCam.read()
    #ret2, frame2 = WebCam.read()
    cv2.imshow('PiCam',  frame)
    #cv2.imshow('WebCam', frame2)
    if cv2.waitKey(1) == ord('q'):
        break
PiCam.release()
#WebCam.release()
cv2.destroyAllWindows()

