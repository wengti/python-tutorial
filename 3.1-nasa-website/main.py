import os
from dotenv import load_dotenv
import requests
import streamlit as st

# Get environmental variables
load_dotenv()

api_key = os.getenv("API_KEY")

response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
content = response.json()

st.title("NASA's Astronomy Picture of the Day (APOD)")
st.subheader(content["title"])
st.video(content["url"], autoplay=True, loop=True, muted=True)
st.text(content["explanation"])
