import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
from autopy.mouse import *
from autopy.key import *
from autopy import *
import pyautogui
import keyboard

def startVirtualMouse():
    ######
    ##########################
    wCam, hCam = 640, 480
    frameR = 100  # Frame Reduction
    smoothening = 7
    #########################

    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    dragging = False

    cap = cv2.VideoCapture(1)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = htm.handDetector(maxHands=1)
    wScr, hScr = autopy.screen.size()
    # print(wScr, hScr)

    while True:
        # 1. Find hand Landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        # 2. Get the tip of the index and middle fingers
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp()

        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                    (255, 0, 255), 2)

        # 4. Only Index Finger : Moving Mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

            length, _, _ = detector.findDistance(8, 4, img)



        # If index finger is closed
        if fingers[1] == 0:
            autopy.mouse.click(button=autopy.mouse.Button.LEFT)


        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:

            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 10. Click mouse if distance short
            if length < 25:
               cv2.circle(img, (lineInfo[4], lineInfo[5]),
                       15, (0, 255, 0), cv2.FILLED)
               autopy.mouse.click(button=autopy.mouse.Button.RIGHT)

        if fingers[1] == 1 and fingers[0] == 1:
            # Find distance between thumb and index finger
            length, _, _ = detector.findDistance(4, 8, img)
            if length < 50:  # Adjust as needed to find a comfortable distance for you
                if not dragging:
                    # Start of drag
                    drag_start_x, drag_start_y = clocX, clocY
                    dragging = True
                    autopy.mouse.toggle(None, True)  # start dragging
            else:
                if dragging:
                    # End of drag
                    dragging = False
                    autopy.mouse.toggle(None, False)  # end dragging

        if fingers[4] == 1 and fingers[1] == 1 :

            # 11. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 12. Scroll mouse if distance short
            autopy.mouse.click(button=autopy.mouse.Button.MIDDLE)

        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 2)
        # 12. Display
        cv2.imshow("Image", img)
        cv2.waitKey(1)

startVirtualMouse()