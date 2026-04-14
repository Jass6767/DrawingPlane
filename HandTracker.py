import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, hands):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=hands)
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        return img

    def get_landmarks(self, img):
        h, w, _ = img.shape
        lm_list = []

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
        return lm_list


