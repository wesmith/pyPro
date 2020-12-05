import cv2
print(cv2.__version__)
scale = 1
dispW = 320 * scale
dispH = 240 * scale
flip = 0
thresh = 200

def nothing():
    pass
cv2.namedWindow('Blended')
cv2.createTrackbar('BlendValue', 'Blended', 50, 100, nothing)

cvLogo = cv2.imread('cv.jpg')
cvLogo = cv2.resize(cvLogo, (dispW, dispH))
cvLogoGray = cv2.cvtColor(cvLogo, cv2.COLOR_BGR2GRAY)
cv2.imshow('cvLogoGray', cvLogoGray)
cv2.moveWindow('cvLogoGray', 0, dispH + 60)

_, BGMask = cv2.threshold(cvLogoGray, thresh, 255, cv2.THRESH_BINARY)
cv2.imshow('Background Mask', BGMask)
cv2.moveWindow('Background Mask', dispW + 70, 0)

FGMask = cv2.bitwise_not(BGMask)
cv2.imshow('Foreground Mask', FGMask)
cv2.moveWindow('Foreground Mask', dispW + 70, dispH + 60)

FG = cv2.bitwise_and(cvLogo, cvLogo, mask=FGMask)
cv2.imshow('FG', FG)
cv2.moveWindow('FG', 2 * dispW + 75, dispH + 60)

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

while True:
    ret, frame = cam.read()

    BG        = cv2.bitwise_and(frame, frame, mask=BGMask)
    compImage = cv2.add(BG, FG)
    BV = cv2.getTrackbarPos('BlendValue', 'Blended')/100
    BV2 = 1 - BV
    Blended   = cv2.addWeighted(frame, BV, FG, BV2, 0)
    FG2       = cv2.bitwise_and(Blended, Blended, mask=FGMask)
    compFinal = cv2.add(BG, FG2)

    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)
    cv2.imshow('BG', BG)
    cv2.moveWindow('BG', 2 * dispW + 75, 0)
    cv2.imshow('Composite', compImage)
    cv2.moveWindow('Composite', 3 * dispW + 80, 0)
    cv2.imshow('Blended', Blended)
    cv2.moveWindow('Blended', 3 * dispW + 80, dispH + 60)
    cv2.imshow('FG2', FG2)
    cv2.moveWindow('FG2', 4 * dispW + 85, 0)
    cv2.imshow('CompositeFinal', compFinal)
    cv2.moveWindow('CompositeFinal', 4 * dispW + 85, dispH + 60)


    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

