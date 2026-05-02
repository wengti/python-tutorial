import streamlit as st
from backend import get_data
import plotly.express as px
import pandas as pd

st.title("Weather Forecast App")
place = st.text_input(label="Enter a place name: ")
nr_days = st.slider(label="Select number of days: ", min_value=1, max_value=5)
config = st.selectbox(
    label="Select the type of data to be viewed: ", options=["Temperature", "Weather"]
)

if place:
    st.subheader(
        f"The weather forecast for {place} in next {nr_days} {"days" if nr_days > 1 else "day"}."
    )

    # Send request to API
    result = get_data(place)
    if result["error"]:
        st.write(
            f":red[Error: {result["error"].response.status_code}: {result["error"].response.reason}]"
        )
    else:
        general_data = result["data"]
        targ_data = general_data["list"][: 8 * nr_days]

        if config == "Temperature":
            dates = [data["dt_txt"] for data in targ_data]
            temperature = [data["main"]["temp"] for data in targ_data]
            df = pd.DataFrame({"Dates": dates, "Temperature": temperature})
            fig = px.line(df, x="Dates", y="Temperature")
            st.plotly_chart(fig)

        elif config == "Weather":
            display_data = [
                {
                    "date": data["dt_txt"],
                    "image": f"https://openweathermap.org/payload/api/media/file/{data["weather"][0]["icon"]}.png",
                }
                for data in targ_data
            ]

            st.image(
                [data["image"] for data in display_data],
                caption=[data["date"] for data in display_data],
            )
