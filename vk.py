import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller, Key

detector = HandDetector(detectionCon=.8, maxHands=2)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P","Del"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", " ",]]

keyboard = Controller()

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1],
                                button.size[0], button.size[0]), 20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 80),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 5)
    return img


class Button():
    def __init__(self, pos, text, size=[80, 80]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


def startVirtualKeyboard():
    cap = cv2.VideoCapture(1)
    cap.set(3, 1280)
    cap.set(4, 720)
    finalText = ""
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)
        img = drawAll(img, buttonList)

        if hands:
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # list of 21 landmarks
            bbox1 = hand1["bbox"]  # bounding box info x,y,w,h

            if len(hands) == 2:
                # Hand 2
                hand2 = hands[1]
                lmList2 = hand2["lmList"]  # List of 21 Landmark points
                bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
                centerPoint2 = hand2['center']  # center of the hand cx,cy
                handType2 = hand2["type"]  # Hand Type "Left" or "Right"

                fingers2 = detector.fingersUp(hand2)

                # Find Distance between two Landmarks. Could be same hand or different hands
                # l, _, _ = detector.findDistance(lmList1[8], lmList2[8], img)  # with draw
                # length, info = detector.findDistance(lmList1[8], lmList2[8])

            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    l, _, _ = detector.findDistance(lmList1[8][1:3], lmList1[4][1:3], img)
                    print(l)

                    if l < 30:
                        if button.text!='Del':
                            keyboard.press(button.text)
                            finalText += button.text
                            print("Pressed", button.text)
                            sleep(0.2)
                        else:
                            if len(finalText) > 0:
                                finalText=finalText[:-1]
                                keyboard.press(Key.backspace)

                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)


        cv2.rectangle(img, (50, 350), (700, 450), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, finalText, (60, 425),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        cv2.imshow("Image", img)
        if cv2.waitKey(5) & 0xFF == 27:
            break


if __name__ == '__main__':
    startVirtualKeyboard()