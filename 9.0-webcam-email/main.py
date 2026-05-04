from pathlib import Path
import threading

import cv2
import numpy as np
from emailing import send_email

cap = cv2.VideoCapture(1)

first_frame = None
has_object_list = []
f_count = 0

images_folder = Path("images")
images_folder.mkdir(parents=True, exist_ok=True)

while True:
    has_object = 0
    f_count += 1

    ret, frame = cap.read()

    # Grayscale image
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blurring
    frame_gray_blur = cv2.GaussianBlur(frame_gray, (21, 21), 0)

    # Save first image as background for comparison
    if first_frame is None:
        first_frame = frame_gray_blur

    # Get absolute difference between current image and background
    diff_between_frames = cv2.absdiff(frame_gray_blur, first_frame)

    # Thresholding the image into either 1 or 0
    _retval, thresholded_diff = cv2.threshold(
        diff_between_frames, 50, 255, cv2.THRESH_BINARY
    )

    # Dilating the white blocks
    kernel = np.ones((5, 5), np.uint8)
    dilated_diff = cv2.dilate(thresholded_diff, kernel, iterations=2)

    # Find contour
    contours, _hierarchy = cv2.findContours(
        dilated_diff, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filter contour and draw rectangles
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        has_object = 1

    # Save the image with rectangle frame if there's detected object
    if has_object:
        cv2.imwrite(f"images/{f_count}.png", frame)

    # Record whether this frame has an object
    has_object_list.append(has_object)

    # If the has_object_list goes from 1 to 0, means that there is no longer a detected object
    if (
        len(has_object_list) >= 2
        and has_object_list[-2] == 1
        and has_object_list[-1] == 0
    ):
        email_thread = threading.Thread(target=send_email)
        email_thread.start()

    # Display the image
    cv2.imshow("Live Webcam", frame)

    # wait for a key for 1ms
    # & 0xFF - bit operator to extract the last 8 bit
    # ord - return the ASCII (int) value of a character
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
