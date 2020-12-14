import face_recognition
import cv2
print('CV2 version {}'.format(cv2.__version__))

base        = '/home/smithw/Devel/jetson_nano/pyPro/faceRecognizer/demoImages/' # WS mod
unknown_dir = base + 'unknown/'
known_dir   = base + 'known/'

donFace   = face_recognition.load_image_file(known_dir + 'Donald Trump.jpg')
donEncode = face_recognition.face_encodings(donFace)[0]

nancyFace   = face_recognition.load_image_file(known_dir + 'Nancy Pelosi.jpg')
nancyEncode = face_recognition.face_encodings(nancyFace)[0]

penceFace   = face_recognition.load_image_file(known_dir + 'Mike Pence.jpg')
penceEncode = face_recognition.face_encodings(penceFace)[0]

Encodings = [donEncode, nancyEncode, penceEncode]
Names     = ['Donald', 'Nancy', 'Mike']

font = cv2.FONT_HERSHEY_SIMPLEX

testImage = face_recognition.load_image_file(unknown_dir + 'u11.jpg')

facePositions = face_recognition.face_locations(testImage)

allEncodings = face_recognition.face_encodings(testImage, facePositions)

testImage = cv2.cvtColor(testImage, cv2.COLOR_RGB2BGR)

# checked online docs: returns (top, right, bottom, left), which is a little weird
for (top, right, bottom, left), face_encoding in zip(facePositions, allEncodings):
    name = 'unknown'
    matches = face_recognition.compare_faces(Encodings, face_encoding)
    if True in matches:
        first_match_index = matches.index(True)
        name = Names[first_match_index]
    cv2.rectangle(testImage, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.putText(testImage, name, (left, top - 6), font, 1, (255, 255, 0), 1)

cv2.imshow('window', testImage)
cv2.moveWindow('window', 0, 0)
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()

