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
    #          to see appropriate variable to add; also see jetsonhacks vids
    camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
    cam = cv2.VideoCapture(camSet)
    fps = cam.get(cv2.CAP_PROP_FPS)  # WS mod 12/21/20
    camNam = 'piCam, FPS = {}'.format(fps)
else:
    # the following is for the webcam: use '1' if picam used in slot '0'
    # note: instead of '1', '/dev/video1' also works, when I tested it
    # from Paul vid 46 comment section (Quaternion), try src = 'rtsp://admin:@10.0.0.6' to
    # acess network cam
    src = 1  # this works
    src = '/dev/video1'  # this works
    #src = 'rtsp://admin:@10.0.0.6'  #this failed
    cam = cv2.VideoCapture(src)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH,  dispW)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
    # WS mod 12/21/20: 5,10,15,20,25,30 fps worked (35 failed, non-powers of 5 failed)
    fps = 30
    cam.set(cv2.CAP_PROP_FPS, fps)  # WS mod 12/21/20
    #fps = cam.get(cv2.CAP_PROP_FPS)  # WS mod 12/21/20: this always shows 7.5 regardless
    camNam = 'webCam, FPS = {}'.format(fps)

actual_dispW = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_dispH = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('')
print('ACTUAL DISPLAY WIDTH, HEIGHT:', actual_dispW, actual_dispH)

while True:
    ret, frame = cam.read()
    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

