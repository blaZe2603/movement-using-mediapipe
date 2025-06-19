import cv2 as cv
import pynput
import finger_position as htm
import time
import threading

# Setup
cap = cv.VideoCapture(1)
keyboard = pynput.keyboard.Controller()
tipIds = [4, 8, 12, 16, 20]
detector = htm.handDetector()
past_time = 0

# Event to stop the thread
stop_event = threading.Event()

def hand_control():
    global past_time
    while not stop_event.is_set():
        success, img = cap.read()
        if not success:
            continue

        current_time = time.time()

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            fingers = []

            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)


            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)


            if current_time - past_time > 0.5:
                past_time = current_time
                key = None
                if totalFingers == 1:
                    key = 'a'
                elif totalFingers == 2:
                    key = 'w'
                elif totalFingers == 3:
                    key = 'd'
                elif totalFingers == 4:
                    key = 's'

                if key:
                    keyboard.press(key)
                    time.sleep(0.3)
                    keyboard.release(key)

                print(f"Fingers: {totalFingers}")


            
            cv.putText(img, str(totalFingers), (45, 375), cv.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

        cv.imshow("Hand Tracker", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()

    cap.release()
    cv.destroyAllWindows()


thread = threading.Thread(target=hand_control)
thread.start()

# Input loop
try:
    while True:
        user_input = input(" ")
        if user_input == 'exit':
            stop_event.set() 
            break
except KeyboardInterrupt:
    stop_event.set()


thread.join()
print("Program exited cleanly.")


