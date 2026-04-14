import time
import cv2
import numpy as np
from HandTracker import HandTracker
from Tools import Tools
from utils import *

tracker = HandTracker(1)
cap = cv2.VideoCapture(0)
alpha = 0.2
smooth_fx, smooth_fy = 0, 0
canvas = np.zeros((480, 640, 3), dtype="uint8")

prev_x, prev_y = 0, 0
prev_circle_centre = (-5, -5)
color = (255, 255, 0)
brush_thickness = 2
Tools = Tools()
fist_start_time = None
fist_triggered = False

icons = {
    "brush" : cv2.resize(
        cv2.imread("icon_pics/paint-palette.png", cv2.IMREAD_UNCHANGED),
        (64, 64)
    ),
    "circle" :  cv2.resize(
        cv2.imread("icon_pics/new-moon.png", cv2.IMREAD_UNCHANGED),
        (64, 64)
    ),
    "square":  cv2.resize(
        cv2.imread("icon_pics/square.png", cv2.IMREAD_UNCHANGED),
        (64, 64)
    ),
}
current_icon = None
icon_timer = 0
icon_duration = 60



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
                current_icon = icons.get(Tools.current_tool, None)
                icon_timer = 15
                fist_triggered = True
        else:
            fist_triggered = False
            fist_start_time = None

        if fingers[0] and fingers[1]:
            prev_x, prev_y = 0, 0

            if y1 < 10:
                if 450 < x1 < 640:
                    canvas = np.zeros((480, 640, 3), np.uint8)
        elif fingers[0] and not fingers[1]:
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x1, y1

            if Tools.current_tool == 'circle':
                if euclidean_distance(prev_circle_centre, (prev_x, prev_y)) > 45:
                    prev_x, prev_y = snap_to_grid_center(prev_x, prev_y, 95)
                    Tools.draw_circle(canvas, (prev_x, prev_y) , 45, color, brush_thickness)
                    prev_circle_centre = (prev_x, prev_y)
            elif Tools.current_tool == 'square':
                if euclidean_distance(prev_circle_centre, (prev_x, prev_y)) > 45:
                    prev_x, prev_y = snap_to_grid_center(prev_x, prev_y, 95)
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
    if current_icon is not None and icon_timer > 0 and lm_list:
        fx, fy = lm_list[0][1], lm_list[0][2] - 100 # wrist

        if abs(fx - smooth_fx) < 3:
            raw_fx = smooth_fx
        if abs(fy - smooth_fy) < 3:
            raw_fy = smooth_fy

        smooth_fx = int(alpha * fx + (1 - alpha) * smooth_fx)
        smooth_fy = int(alpha * fy + (1 - alpha) * smooth_fy)

        fx, fy = smooth_fx, smooth_fy


        progress = 1 - (icon_timer / icon_duration)

        offset_y = int(progress * 50)

        scale = 0.5 + 0.5 * progress

        icon_resized = cv2.resize(current_icon, None, fx=scale, fy=scale)

        h, w = icon_resized.shape[:2]

        x = fx - w // 2
        y = fy - offset_y - h // 2

        img = overlay_png(img, icon_resized, x, y)

        icon_timer -= 1

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
