import cv2 as cv
import numpy as np
import mediapipe as mp



mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

video = cv.VideoCapture(0)


with mp_holistic.Holistic(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as holistic:


    while True:

        _ , frame = video.read()
        
        image = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

        
        results = holistic.process(image)

        image = cv.cvtColor(image,cv.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)

        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        print(results)            
        
        cv.imshow("Holistic Modelq",image) 

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv.destroyAllWindows()