# train_write.py  save face-recognizer training
# WS made this a module 12/24/20
# removed Bill Barr image from training set: 4MB

# Paul McWhorter vid 41

import face_recognition
import os
import pickle

def train_write(training):

    Encodings = []
    Names     = []

    for root, dirs, files in os.walk(training):
        #print(root, dirs, files)
        for file in files:
            path = os.path.join(root, file)
            #print(path)
            if os.path.splitext(file)[1] == '.pkl': 
                continue  # skip training file in same directory as imagery
            name = os.path.splitext(file)[0]
            print('training', name, os.path.splitext(file)[1])

            person   = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(person)[0]
            Encodings.append(encoding)
            Names.append(name)

    with open(os.path.join(training,'train.pkl'), 'wb') as f:
        pickle.dump(Names, f)
        pickle.dump(Encodings, f)


if __name__ == "__main__":
    
    training_dir = '/home/smithw/Devel/jetson_nano/pyPro/faceRecognizer/demoImages/known'
    train_write(training_dir)
