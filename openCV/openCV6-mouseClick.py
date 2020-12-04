import cv2
import numpy as np
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0
evt  = -1
coord = []
img  = np.zeros((64, 256, 3), np.uint8)

picam = True # WS mod

if picam: 
    # gstreamer command line for pi camera
    # WS note: picam is hooked to '0' connector, the other is '1': apparently '0' runs by default
    #          if a second picam is used and hooked to '1' slot, then need to add a new
    #          channel variable to the command below: see comments in McWhorter vid (which one?)
    #          to see appropriate variable to add
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    cam = cv2.VideoCapture(camSet)
    camNam = 'piCam'
else:
    # the following is for the webcam: use '1' if picam used in slot '0'
    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,  dispW)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
    camNam = 'webCam'

actual_dispW = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_dispH = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('')
print('ACTUAL DISPLAY WIDTH, HEIGHT:', actual_dispW, actual_dispH)

def click(event, x, y, flags, params):
    global pnt  # explictly global because of callback? won't work if defined at top
    global evt  # ditto
    if event == cv2.EVENT_LBUTTONDOWN:
        #print('mouse event was: ', event, 'x, y: ', x, y)
        pnt = (x, y)
        coord.append(pnt)
        #print(coord)
        evt = event
    if event == cv2.EVENT_RBUTTONDOWN:
        blue, green, red = frame[y, x, :]  # WS mod
        #print(blue, green, red)
        colorString = str(blue) + ',' + str(green) + ',' + str(red)
        img[:] = [blue, green, red]
        fnt = cv2.FONT_HERSHEY_PLAIN
        tp = (255-int(blue), 255-int(green), 255-int(red))  # inverse color
        cv2.putText(img, colorString, (10, 25), fnt, 2, tp, 2)
        cv2.imshow('myColor', img)
        cv2.moveWindow('myColor', 0, dispH + 100)

cv2.namedWindow(camNam)
cv2.setMouseCallback(camNam, click)
font = cv2.FONT_HERSHEY_PLAIN
showText = False

while True:
    ret, frame = cam.read()

    for pnts in coord:
        cv2.circle(frame, pnts, 5, (0, 255, 0), -1)
        if showText:
            myStr = str(pnts)
            cv2.putText(frame, myStr, pnts, font, 1, (0, 0, 255), 1)

    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    keyEvent = cv2.waitKey(1)
    if keyEvent == ord('q'):
        break
    if keyEvent == ord('c'):
        coord = []
    if keyEvent == ord('t'): # WS mod
        showText = not showText

cam.release()
cv2.destroyAllWindows()

