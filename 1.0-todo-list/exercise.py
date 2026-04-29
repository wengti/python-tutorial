# Note: This script runs only on a local IDE with "streamlit run main.py"
import streamlit as st
from PIL import Image

st.subheader("Color to Grayscale Converter")

with st.expander("Start camera"):
    camera_image = st.camera_input("Camera")

with st.expander("Upload image"):
    uploaded_image = st.file_uploader("Choose a file")

if camera_image:
    img = Image.open(camera_image)
    gray_camera_img = img.convert("L")
    st.image(gray_camera_img)

if uploaded_image:
    u_img = Image.open(uploaded_image)
    gray_u_img = u_img.convert("L")
    st.image(gray_u_img)
