# read_recognize.py  read and test face-recognizer training
# WS made this a module 12/24/20
# removed Bill Barr image from training set: 4MB

# Paul McWhorter vid 41

import face_recognition
import cv2
import os
import pickle

def read_recognize(training_file, testing_dir):

    with open(training_file, 'rb') as f:
        Names     = pickle.load(f)
        Encodings = pickle.load(f)

    font = cv2.FONT_HERSHEY_SIMPLEX

    for root, dirs, files in os.walk(testing_dir):
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
                scor  = ''

                # WS mod: examine distances to training faces: better to choose smallest distance
                #         than to randomly take first True match from the list
                distances = face_recognition.face_distance(Encodings, face_encoding)
                min_dist  = distances.min()

                if min_dist < 0.6: # considered a match if true
                    index_of_min = distances.argmin()  # WS mod: choose smallest distance
                    name  = '{}'.format(Names[index_of_min])
                    scor  = '{:2.2f}'.format(min_dist)
                cv2.rectangle(testImage, (left, top), (right, bottom), (0, 0, 255), 2)
                #cv2.rectangle(testImage, (left, top - 50), (left + 200, top-5), (0, 0, 0), -1)
                cv2.putText(testImage, name, (left, top - 10), font, 0.75, (0, 255, 255), 3)
                cv2.putText(testImage, scor, (left, top - 30), font, 0.75, (0, 255, 255), 3)
                cv2.putText(testImage, name, (left, top - 10), font, 0.75, (0, 0, 0), 2)
                cv2.putText(testImage, scor, (left, top - 30), font, 0.75, (0, 0, 0), 2)


            cv2.imshow('window', testImage)
            cv2.moveWindow('window', 0, 0)

            if cv2.waitKey(0) == ord('q'):  # 0: hold image until key is pressed
                cv2.destroyAllWindows()


if __name__ == "__main__":
    
    training_file = '/home/smithw/Devel/jetson_nano/pyPro/faceRecognizer/demoImages/known/train.pkl'
    testing_dir  = '/home/smithw/Devel/jetson_nano/pyPro/faceRecognizer/demoImages/unknown'
    read_recognize(training_file, testing_dir)


