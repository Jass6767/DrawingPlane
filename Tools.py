# Define tools here
from asyncio import current_task

import cv2
import time
from typing import Tuple

class Tools:
    def __init__(self):
        self.current_tool = 'brush'
        self.tool_index = 0
        self.rect_active = False
        self.rect_start_time = None

    def change_tools(self):
        if self.tool_index == 0:
            self.current_tool = 'circle'
            self.tool_index = 1
        elif self.tool_index == 1:
            self.current_tool = 'square'
            self.tool_index = 2
        else:
            self.current_tool = 'brush'
            self.tool_index = 0

    def get_tools_list(self):
        pass

    def draw_circle(self, img, center, radius, color, thickness):
        neon = color
        fill = tuple(int(c * 0.5) for c in color)

        cv2.circle(img, center, radius, neon, thickness-1)

        cv2.circle(img, center, radius - thickness, fill, -1)

    def draw_square(self, img, points, color, thickness):
        neon = color
        fill = tuple(int(c * 0.5) for c in color)
        diff = 40

        cv2.rectangle(img, (points[0] - diff, points[1] - diff), (points[0]+50, points[1]+50), neon, thickness)
        cv2.rectangle(img, (points[0] - diff, points[1] - diff), (points[0] + 50, points[1] + 50), fill, -1)

    def draw_brush(self,canvas, prev: Tuple, x: Tuple , color, brush_thickness):
        cv2.line(canvas, (prev[0], prev[1]), (x[0], x[1]), color, brush_thickness)


