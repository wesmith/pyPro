import cv2
print(cv2.__version__)
scale = 2
dispW = 320 * scale
dispH = 240 * scale
flip = 0

picam    = True # WS mod
fromFile = True # WS mod this overrides cameras, plays movie from a file
delay    = 1     # WS mod: no delay if live feed, delay if from file
savNam   = 'videos/myCam.avi'  # WS mod

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

if fromFile: #override cameras  WS mod
    camNam = savNam
    cam = cv2.VideoCapture(savNam)
    delay = 50

if not fromFile:
    outVid = cv2.VideoWriter(savNam, cv2.VideoWriter_fourcc(*'XVID'), 21, (dispW, dispH))

while True:
    ret, frame = cam.read()
    #print(ret)
    if fromFile and not ret: # WS added ret check if reading from a file
        break
    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)
    if not fromFile:
        outVid.write(frame)
    if cv2.waitKey(delay) == ord('q'):
        break
cam.release()
if not fromFile:
    outVid.release()
cv2.destroyAllWindows()

