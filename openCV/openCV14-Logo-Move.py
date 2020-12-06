import cv2
import numpy as np
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0

picam = True # WS mod

BW, BH = 100, 100  # WS mod
PL = cv2.imread('pl.jpg')
PL = cv2.resize(PL, (BW, BH))
cv2.imshow('LogoWindow', PL)
cv2.moveWindow('LogoWindow', dispW + BW, 0)

PLGray = cv2.cvtColor(PL, cv2.COLOR_BGR2GRAY)
cv2.imshow('LogoGray', PLGray)
cv2.moveWindow('LogoGray', dispW + 2*BW, 0)

_, BGMask = cv2.threshold(PLGray, 245, 255, cv2.THRESH_BINARY)
kernel = np.ones((3,3), np.uint8)  # WS mod
BGMask = cv2.dilate(BGMask, kernel, iterations=1)  # WS mod to clean up edges
cv2.imshow('BGMask', BGMask)
cv2.moveWindow('BGMask', dispW + 3*BW, 0)

FGMask = cv2.bitwise_not(BGMask)
#FGMask = cv2.erode(FGMask, kernel, iterations=1)  # WS mod to clean up edges
cv2.imshow('FGMask', FGMask)
cv2.moveWindow('FGMask', dispW + 4*BW, 0)

FG = cv2.bitwise_and(PL, PL, mask=FGMask)
cv2.imshow('FG', FG)
cv2.moveWindow('FG', dispW + 5*BW, 0)

Xpos, Ypos = 10, 10
dX, dY     =  5,  5

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

while True:
    ret, frame = cam.read()

    #print(Xpos, Xpos + BW, Ypos, Ypos + BH)
    ROI = frame[Ypos:Ypos + BH, Xpos:Xpos + BW]
    ROIBG = cv2.bitwise_and(ROI, ROI, mask=BGMask)
    cv2.imshow('ROIBG', ROIBG)
    cv2.moveWindow('ROIBG', dispW + 6*BW, 0)

    ROInew = cv2.add(FG, ROIBG)
    cv2.imshow('ROInew', ROInew)
    cv2.moveWindow('ROInew', dispW + 7*BW, 0)

    frame[Ypos:Ypos + BH, Xpos:Xpos + BW] = ROInew

    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    Xpos += dX
    Ypos += dY
    # WS modded the below checks for more precision
    if Xpos < 0 or Xpos + BW > dispW - 1: 
        dX *= -1
        Xpos += dX  # reset
    if Ypos <= 0 or Ypos + BH >= dispH - 1: 
        dY *= -1
        Ypos += dY  # reset
 
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

