import cv2
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

BW = int(.15 * actual_dispW)
BH = int(.25 * actual_dispH)
posX =  10
posY = 270
dX = 4
dY = 4

while True:
    ret, frame = cam.read()
    cv2.moveWindow(camNam, 0, 0)

    # ws mod: added color dependent upon position
    frame = cv2.rectangle(frame, (posX, posY), (posX + BW, posY + BH), (posX, posY, posX + posY), -1)
    cv2.imshow(camNam, frame)
    posX += dX
    posY += dY
    if (posX <= 0) or (posX + BW) >= actual_dispW: dX *= -1
    if (posY <= 0) or (posY + BH) >= actual_dispH: dY *= -1

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

