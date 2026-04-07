import cv2
import numpy as np
from HandTracker import HandTracker

tracker = HandTracker(1)
cap = cv2.VideoCapture(0)

canvas = np.zeros((480, 640, 3), dtype="uint8")

prev_x, prev_y = 0, 0
color = ( 255, 200, 149)
brush_thickness = 2

def fingers_up(lm_list):
    fingers = [lm_list[8][2] < lm_list[6][2], lm_list[12][2] < lm_list[10][2]]
    return fingers


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.find_hands(img)
    lm_list = tracker.get_landmarks(img)

    if lm_list:
        x1, y1 = lm_list[8][1], lm_list[8][2]
        x2, y2 = lm_list[12][1], lm_list[12][2]

        fingers = fingers_up(lm_list)

        if fingers[0] and fingers[1]:
            prev_x, prev_y = 0, 0

            if y1 < 50:
                if 0 < x1 < 150:
                    color = (255, 0, 0)  # Blue

                elif 150 < x1 < 300:
                    color = (0, 255, 0)  # Green

                elif 300 < x1 < 450:
                    color = (0, 0, 255)  # Red

                elif 450 < x1 < 640:
                    canvas = np.zeros((480, 640, 3), np.uint8)
        elif fingers[0] and not fingers[1]:
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x1, y1

            cv2.line(canvas, (prev_x, prev_y), (x1, y1), color, brush_thickness)
            prev_x, prev_y = x1, y1

    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    # UI bar
    cv2.rectangle(img, (0, 0), (150, 50), (255, 0, 0), -1)
    cv2.rectangle(img, (150, 0), (300, 50), (0, 255, 0), -1)
    cv2.rectangle(img, (300, 0), (450, 50), (0, 0, 255), -1)
    cv2.rectangle(img, (450, 0), (640, 50), (0, 0, 0), -1)
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (0, 9), (9, 10), (10, 11), (11, 12),
        (0, 13), (13, 14), (14, 15), (15, 16),
        (0, 17), (17, 18), (18, 19), (19, 20)
    ]
    for start, end in connections:
        if lm_list and len(lm_list) > start:
            x1, y1 = lm_list[start][1], lm_list[start][2]
            x2, y2 = lm_list[end][1], lm_list[end][2]
            cv2.line(img, (x1, y1), (x2, y2), ( 255, 200, 149), 2)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break