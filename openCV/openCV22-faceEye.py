import cv2
print(cv2.__version__)
scale = 1
dispW = 320 * scale
dispH = 240 * scale
flip = 0

picam = False # WS mod  the face-detection latency is best with logitech camera (picam = False)
alpha = 0.2   # WS mod: smoothing factor for tracking, (0,1): alpha = 0 means no smoothing

face_cascade = cv2.CascadeClassifier('cascade/face.xml')
eye_cascade  = cv2.CascadeClassifier('cascade/eye.xml')

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

objX, objY = 0, 0  # WS mod for implementing smoother

while True:
    ret, frame = cam.read()

    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        objX = alpha * objX + (1 - alpha) * (x + w/2)  # WS mod to smooth centroid
        objY = alpha * objY + (1 - alpha) * (y + h/2)  # WS mod
        cv2.circle(frame, (int(objX), int(objY)), 5, (0, 255, 255), -1) # WS mod
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        roi_gray  = gray[y:y + h, x:x + w]
        eyes  = eye_cascade.detectMultiScale(roi_gray)

        # make roi a reference to frame, not a copy, so that circles will end up on the frame
        roi_color = frame[y:y + h, x:x + w]
        
        for (xEye, yEye, wEye, hEye) in eyes:
            xE = int(xEye + wEye/2)
            yE = int(yEye + hEye/2)
            # rule out nostril detections: eyes are above face center; yE + y is relative to the frame
            if yE + y < objY:  
                cv2.circle(roi_color, (xE, yE), 10, (0, 0, 255), -1)

    cv2.imshow(camNam, frame)
    cv2.moveWindow(camNam, 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

