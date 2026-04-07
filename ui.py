import cv2
import math
import time

start_time = time.time()

def draw_ui(frame, faces, names, verified_list, current_challenge, status_msg):

    # ===== ANIMATION VALUE =====
    t = time.time() - start_time
    pulse = int((math.sin(t * 3) + 1) * 50)  # smooth animation

    # ===== TOP BAR =====
    cv2.rectangle(frame, (0,0), (frame.shape[1], 60), (30,30,30), -1)

    cv2.putText(frame, f"Do: {current_challenge}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,150+pulse,255), 3)

    # ===== STATUS MESSAGE =====
    cv2.putText(frame, status_msg, (20,90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

    # ===== FACE BOXES =====
    for i, ((top, right, bottom, left), name) in enumerate(zip(faces, names)):

        verified = verified_list[i] if i < len(verified_list) else False

        color = (0,255,0) if verified else (0,0,255)

        thickness = 2 + pulse//25  # animated border

        cv2.rectangle(frame, (left, top), (right, bottom), color, thickness)

        # Name background
        cv2.rectangle(frame, (left, top-30), (right, top), color, -1)

        cv2.putText(frame, name, (left+5, top-8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    return frame