# Define tools here
import cv2
import time
from typing import Tuple

class Tools:
    def __init__(self):
        self.current_tool = 'circle'
        self.tool_index = 0

    def change_tools(self):
        pass

    def get_tools_list(self):
        pass

    def draw_circle(self, img, center, radius, color, thickness):
        cv2.circle(img, center, radius, color, thickness)

    def draw_square(self, img, points, color, thickness):
        cv2.rectangle(img, (points[0] -50, points[1] -50), (points[0]+50, points[1]+50), color, thickness)

    def draw_brush(self,canvas, prev: Tuple, x: Tuple , color, brush_thickness):
        cv2.line(canvas, (prev[0], prev[1]), (x[0], x[1]), color, brush_thickness)


