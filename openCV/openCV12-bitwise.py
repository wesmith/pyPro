import cv2
import numpy as np
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0

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

img1 = np.zeros((dispH, dispW, 1), np.uint8)
img1[:, 0:int(dispW/2)] = 255
img2 = np.zeros((dispH, dispW, 1), np.uint8)
centerX, centerY = int(dispW/2), int(dispH/2)
boxW = 100
offset = int(boxW/2)
img2[centerY-offset:centerY+offset, centerX-offset:centerX+offset] = 255

bitAnd = cv2.bitwise_and(img1, img2)
bitOr  = cv2.bitwise_or(img1, img2)
bitXor = cv2.bitwise_xor(img1, img2)

while True:
    ret, frame = cam.read()

    cv2.imshow('img1', img1)
    cv2.moveWindow('img1', 0, dispH + 50)
    cv2.imshow('img2', img2)
    cv2.moveWindow('img2', dispW + 50, 0)
    #cv2.imshow('AND', bitAnd)
    #cv2.moveWindow('AND', dispW + 50, dispH + 50)
    #cv2.imshow('OR', bitOr)
    #cv2.moveWindow('OR', dispW + 50, dispH + 50)
    cv2.imshow('XOR', bitXor)
    cv2.moveWindow('XOR', dispW + 50, dispH + 50)

    frame = cv2.bitwise_and(frame, frame, mask=bitXor)
    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

