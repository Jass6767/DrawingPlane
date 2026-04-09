import time

import cv2
import numpy as np
from HandTracker import HandTracker
from Tools import Tools

tracker = HandTracker(1)
cap = cv2.VideoCapture(0)

canvas = np.zeros((480, 640, 3), dtype="uint8")

prev_x, prev_y = 0, 0
prev_circle_centre = (-5, -5)
color = (255, 200, 149)
brush_thickness = 2
Tools = Tools()
fist_start_time = None
fist_triggered = False

def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5

def fingers_up(lm_list):
    fingers = [lm_list[8][2] < lm_list[6][2], lm_list[12][2] < lm_list[10][2]]
    return fingers

def is_fist(lm_list):
    if not lm_list or len(lm_list) < 21:
        return False

    fingers_down = [
        lm_list[8][2] > lm_list[6][2],    # index
        lm_list[12][2] > lm_list[10][2],  # middle
        lm_list[16][2] > lm_list[14][2],  # ring
        lm_list[20][2] > lm_list[18][2],  # pinky
    ]

    return all(fingers_down)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.find_hands(img)
    lm_list = tracker.get_landmarks(img)

    if lm_list:
        x1, y1 = lm_list[8][1], lm_list[8][2]
        x2, y2 = lm_list[12][1], lm_list[12][2]

        fingers = fingers_up(lm_list)

        if is_fist(lm_list):
            if fist_start_time is None:
                fist_start_time = time.time()

            elapsed_time = time.time() - fist_start_time

            if elapsed_time > 1 and not fist_triggered:
                Tools.change_tools()
                fist_triggered = True
        else:
            fist_triggered = False
            fist_start_time = None

        if fingers[0] and fingers[1]:
            prev_x, prev_y = 0, 0

            if y1 < 10:
                if 0 < x1 < 150:
                    color = (255, 0, 0)

                elif 150 < x1 < 300:
                    color = (0, 255, 0)

                elif 300 < x1 < 450:
                    color = (0, 0, 255)

                elif 450 < x1 < 640:
                    canvas = np.zeros((480, 640, 3), np.uint8)
        elif fingers[0] and not fingers[1]:
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x1, y1

            if Tools.current_tool == 'circle':
                if euclidean_distance(prev_circle_centre, (prev_x, prev_y)) > 45:
                    Tools.draw_circle(canvas, (prev_x, prev_y) , 45, color, brush_thickness)
                    prev_circle_centre = (prev_x, prev_y)
            elif Tools.current_tool == 'square':
                if euclidean_distance(prev_circle_centre, (prev_x, prev_y)) > 45:
                    Tools.draw_square(canvas, (prev_x, prev_y), color, brush_thickness)
                    prev_circle_centre = (prev_x, prev_y)
            else:
                Tools.draw_brush(canvas, (prev_x, prev_y), (x1, y1), color, brush_thickness)
            prev_x, prev_y = x1, y1


    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, inv)
    img = cv2.bitwise_or(img, canvas)

    # UI bar
    cv2.rectangle(img, (0, 0), (150, 10), (255, 0, 0), -1)
    cv2.rectangle(img, (150, 0), (300, 10), (0, 255, 0), -1)
    cv2.rectangle(img, (300, 0), (450, 10), (0, 0, 255), -1)
    cv2.rectangle(img, (450, 0), (640, 10), (0, 0, 0), -1)
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
            cv2.line(img, (x1, y1), (x2, y2), (255, 200, 149), 2)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
