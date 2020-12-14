import face_recognition
import cv2
print('CV2 version {}'.format(cv2.__version__))

base        = '/home/smithw/Devel/jetson_nano/pyPro/faceRecognizer/demoImages/' # WS mod
unknown_dir = base + 'unknown/'
image = face_recognition.load_image_file(unknown_dir + 'u3.jpg')

face_locations = face_recognition.face_locations(image)
print(face_locations)

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# checked online docs: returns (top, right, bottom, left), which is a little weird
for (top, right, bottom, left) in face_locations:
    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

cv2.imshow('window', image)
cv2.moveWindow('window', 0, 0)
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()


