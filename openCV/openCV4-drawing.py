import cv2
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0

picam = True # WS mod

if picam: 
    # gstreamer command line for pi camera
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    cam = cv2.VideoCapture(camSet)
    camNam = 'piCam'
else:
    # the following is for the webcam
    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,  dispW)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
    camNam = 'webCam'

rx = 110
ry = 70
fnt = cv2.FONT_HERSHEY_DUPLEX
while True:
    ret, frame = cam.read()
    frame = cv2.rectangle(frame, (140, 100), (140 + rx, 100 + ry), (0, 255, 0), 7)
    frame = cv2.circle(frame, (140, 100), 50, (255, 255, 0), -1)
    frame = cv2.putText(frame, 'Testing', (300, 300), fnt, 1.5, (150, 0, 255), 2)
    frame = cv2.line(frame, (10, 10), (630, 470), (100, 200, 100), 4)
    frame = cv2.arrowedLine(frame, (10, 470), (630, 10), (200, 100, 50), 4)
    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

