def snap_to_grid_center(x, y, grid_size):
    cell_x = x // grid_size
    cell_y = y // grid_size

    center_x = cell_x * grid_size + grid_size // 2
    center_y = cell_y * grid_size + grid_size // 2

    return center_x, center_y

def overlay_png(bg, overlay, x, y):
    h, w = overlay.shape[:2]

    # clip region to stay inside background
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(bg.shape[1], x + w), min(bg.shape[0], y + h)

    # adjust overlay region accordingly
    overlay_x1 = x1 - x
    overlay_y1 = y1 - y
    overlay_x2 = overlay_x1 + (x2 - x1)
    overlay_y2 = overlay_y1 + (y2 - y1)

    if x1 >= x2 or y1 >= y2:
        return bg  # nothing to draw

    roi = bg[y1:y2, x1:x2]
    overlay_crop = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]

    overlay_rgb = overlay_crop[:, :, :3]
    mask = overlay_crop[:, :, 3] / 255.0

    for c in range(3):
        roi[:, :, c] = (1 - mask) * roi[:, :, c] + mask * overlay_rgb[:, :, c]
    bg[y1:y2, x1:x2] = roi
    return bg

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