from datetime import datetime

import streamlit as st
import cv2

st.title("Adding date to the webcam")
opened = st.button("Turn on the webcam")
closed = st.button("Turn off the webcam")
image_spot = st.empty()


if opened:
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        cv2.putText(frame, now, (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        with image_spot:
            st.image(frame, channels="BGR")

elif closed:
    pass
