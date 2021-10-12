import cv2
import hand_tracking_module as mp
import os
import random
from pygame import mixer
import time
import cvzone

mixer.init()
winsound = mixer.Sound('win.mp3')
losesound = mixer.Sound('lose.mp3')
f = 0
my_choice = 99
timenow = 0
stage = 0
cap = cv2.VideoCapture(1) #external cam
# resize the cam
cap.set(3, 1500)  # 3 is the nb of the width
cap.set(4, 480)  # 4 is the nb of the heigths

folderPath = "hand icons"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
result = ''
my_score = 0
pc_score = 0
for i in myList:
    image = cv2.imread(f'{folderPath}/{i}', cv2.IMREAD_UNCHANGED)
    overlayList.append(image)

detector = mp.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

currenttime = time.time()
thumb = cv2.imread('thmub.png', cv2.IMREAD_UNCHANGED)
while True:
    success, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    # print(lmList)
    cv2.putText(frame, str(my_score), (550, 150), cv2.FONT_HERSHEY_PLAIN, 6, (100, 0, 255), 8)
    cv2.putText(frame, str(pc_score), (650, 150), cv2.FONT_HERSHEY_PLAIN, 6, (100, 0, 255), 8)
    cv2.putText(frame, '-', (605, 140), cv2.FONT_HERSHEY_PLAIN, 4, (100, 0, 255), 5)
    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[4]][1]:
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:  # if 4 is on the left of 3 then it is closed)
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:  # if 4 is on the left of 3 then it is closed)
                fingers.append(1)
            else:
                fingers.append(0)

        # other fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]: #landmark 8 and 6 and get the value of the y  (the max value at the max height is 0 : start from the top)
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        if totalFingers == 5:
            # cv2.putText(frame, "paper", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
            # frame[0:289, 0:200] = overlayList[0]
            frame = cvzone.overlayPNG(frame, overlayList[0], [0, 0])
            my_choice = 0

        elif totalFingers == 0:
            # cv2.putText(frame, "rock", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
            # frame[0:289, 0:200] = overlayList[1]
            frame = cvzone.overlayPNG(frame, overlayList[1], [0, 0])
            my_choice = 1

        elif (totalFingers == 2) & (lmList[tipIds[1]][2] < lmList[tipIds[1] - 2][2]) & (
                lmList[tipIds[2]][2] < lmList[tipIds[2] - 2][2]):
            # cv2.putText(frame, "Scissors", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
            # frame[0:289, 0:200] = overlayList[2]
            frame = cvzone.overlayPNG(frame, overlayList[2], [0, 0])
            my_choice = 2

        else:
            # cv2.putText(frame, "nothing", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
            my_choice = 3

            # print(totalFingers)
        # cv2.putText(frame, str(totalFingers), (45,375), cv2.FONT_HERSHEY_PLAIN, 10, (2500,0,255), 25)

    # frame[0:289, 1080:1280] = random.choice(overlayList)
    timenow = time.time() - currenttime
    if (timenow < 5):
        # frame[0:289, 1080:1280] = random.choice(overlayList)
        frame = cvzone.overlayPNG(frame, random.choice(overlayList), [1080, 0])
        cv2.putText(frame, str(round(5 - timenow)), (1150, 400), cv2.FONT_HERSHEY_PLAIN, 6, (2500, 0, 255), 5)
    elif (timenow >= 5) & (timenow < 10) & (stage == 0):
        stage = 1
        pc_choice = random.randint(0, 2)
        # frame[0:289, 1080:1280] = overlayList[pc_choice]
        frame = cvzone.overlayPNG(frame, overlayList[pc_choice], [1080, 0])
    else:
        # frame[0:289, 1080:1280] = overlayList[pc_choice]
        frame = cvzone.overlayPNG(frame, overlayList[pc_choice], [1080, 0])

    if (stage == 1):
        if (pc_choice == 0):
            if (my_choice == 0):
                # cv2.putText(frame, "EQUAL", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "EQUAL"
            elif (my_choice == 1):
                # cv2.putText(frame, "LOSE", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "LOSE"
                pc_score = pc_score + 1
            elif (my_choice == 2):
                # cv2.putText(frame, "WIN", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "WIN"
                my_score = my_score + 1
            else:
                # cv2.putText(frame, "nothing ", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "RETRY"
        if (pc_choice == 1):
            if (my_choice == 0):
                # cv2.putText(frame, "WIN", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "WIN"
                my_score = my_score + 1
            elif (my_choice == 1):
                # cv2.putText(frame, "EQUAL", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "EQUAL"
            elif (my_choice == 2):
                # cv2.putText(frame, "LOSE", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "LOSE"
                pc_score = pc_score + 1
            else:
                # cv2.putText(frame, "nothing ", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "RETRY"

        if (pc_choice == 2):
            if (my_choice == 0):
                # cv2.putText(frame, "LOSE", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "LOSE"
                pc_score = pc_score + 1
            elif (my_choice == 1):
                # cv2.putText(frame, "WIN", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "WIN"
                my_score = my_score + 1
            elif (my_choice == 2):
                # cv2.putText(frame, "EQUAL", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "EQUAL"
            else:
                # cv2.putText(frame, "nothing ", (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (100, 0, 255), 10)
                result = "RETRY"
        stage = 2
    if (stage == 2) & (timenow < 10):
        if (my_score < 3) & (pc_score < 3):
            cv2.putText(frame, result, (580, 600), cv2.FONT_HERSHEY_PLAIN, 4, (200, 0, 0), 4)
        elif (my_score == 3):
            cv2.putText(frame, 'Congratulations You just ', (200, 600), cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 0), 4)
            cv2.putText(frame, 'won The Game.', (350, 650), cv2.FONT_HERSHEY_PLAIN, 4, (0, 200, 0), 4)
            if (f == 0):
                f = 1
                winsound.play(0)
        elif (pc_score == 3):
            cv2.putText(frame, 'Sorry You just lost The Game.', (150, 600), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 200), 4)
            cv2.putText(frame, 'Please try again...', (350, 650), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 200), 4)
            if (f == 0):
                f = 1
                losesound.play(0)

    if (stage == 2) & (timenow >= 10):
        f = 0
        stage = 0
        timenow = 0
        currenttime = time.time()
        if (pc_score == 3) | (my_score == 3):
            my_score = 0
            pc_score = 0

    cv2.imshow("Rock Paper Scissors", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
