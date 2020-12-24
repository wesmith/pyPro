# Paul McWhorter vid 41

import face_recognition
import cv2
import os
import pickle

print('CV2 version {}'.format(cv2.__version__))

Encodings = []
Names     = []
j = 0

base      = '/home/smithw/Devel/jetson_nano/pyPro/faceRecognizer/demoImages/' # WS mod
image_dir = base + 'known/'
unkn_dir  = base + 'unknown/'

for root, dirs, files in os.walk(image_dir):
    #print(files)
    for file in files:
        path = os.path.join(root, file)
        #print(path)
        name = os.path.splitext(file)[0]
        print('training', name)

        person   = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(person)[0]
        Encodings.append(encoding)
        Names.append(name)

with open('train.pkl', 'wb') as f:
    pickle.dump(Names, f)
    pickle.dump(Encodings, f) 

# zero out to test
Names     = []
Encodings = []

with open('train.pkl', 'rb') as f:
    Names     = pickle.load(f)
    Encodings = pickle.load(f)

font = cv2.FONT_HERSHEY_SIMPLEX

for root, dirs, files in os.walk(unkn_dir):
    for file in files:
        path = os.path.join(root, file)
        #print(path)
        name = os.path.splitext(file)[0]
        print('testing', name)

        testImage = face_recognition.load_image_file(path)

        facePositions = face_recognition.face_locations(testImage)
        allEncodings  = face_recognition.face_encodings(testImage, facePositions)

        testImage = cv2.cvtColor(testImage, cv2.COLOR_RGB2BGR)

        for (top, right, bottom, left), face_encoding in zip(facePositions, allEncodings):

            name  = 'unknown'

            # WS note: compare_faces uses a default distance of 0.6 to be considered a match
            #matches = face_recognition.compare_faces(Encodings, face_encoding)

            # WS mod: examine distances to training faces: better to choose smallest distance
            #         than to randomly take first True match from the list
            distances = face_recognition.face_distance(Encodings, face_encoding)
            min_dist  = distances.min()

            if min_dist < 0.6: # considered a match if true
            #if True in matches:
                #first_match_index = matches.index(True)
                #name  = Names[first_match_index]
                index_of_min = distances.argmin()  # WS mod: choose smallest distance
                name  = '{}: {:2.2f}'.format(Names[index_of_min], min_dist)
            cv2.rectangle(testImage, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(testImage, name, (left, top - 6), font, 1, (100, 255, 255), 1)

        cv2.imshow('window', testImage)
        cv2.moveWindow('window', 0, 0)

        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows()
















