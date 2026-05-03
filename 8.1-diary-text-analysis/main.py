from datetime import datetime
import os
import streamlit as st
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import pandas as pd
import plotly.express as px

nltk.download("vader_lexicon")

if not os.path.exists("data.txt"):
    with open("data.txt", "w") as f:
        f.write("\n")

analyzer = SentimentIntensityAnalyzer()

st.title("Your Diary Analysis")
user_entry = st.text_area(label="Your thoughts: ").strip(" \n")
if user_entry:
    with open("data.txt", "a") as f:
        f.write("Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("Thoughts: \n")
        f.write(user_entry + "\n")
        score = analyzer.polarity_scores(user_entry)
        f.write(f"Positive Score: {score['pos']}\n")
        f.write(f"Negative Score: {score['neg']}\n")
        f.write("\n")


with open("data.txt", "r") as f:
    all_entry = f.read()

if len(all_entry) > 1:
    dates = re.findall("\nDate: (.*)\n", all_entry)
    user_records = re.findall("\nThoughts: \n(.*)\n", all_entry)
    positive_scores = re.findall("\nPositive Score: (.*)\n", all_entry)
    negative_scores = re.findall("\nNegative Score: (.*)\n", all_entry)

    for i in range(len(dates)):
        positive_color = "green" if float(positive_scores[i]) > 0.5 else "blue"
        negative_color = "red" if float(negative_scores[i]) > 0.5 else "blue"

        st.caption(dates[i])
        st.subheader(user_records[i])
        l_col, r_col = st.columns(2, border=True)
        with l_col:
            st.write(f"Positive Score: :{positive_color}[{positive_scores[i]}]")
        with r_col:
            st.write(f"Negative Score: :{negative_color}[{negative_scores[i]}]")
        st.write("\n")

    if len(dates) > 1:
        df = pd.DataFrame(
            {
                "Date": dates,
                "Positive Scores": [float(score) for score in positive_scores],
                "Negative Scores": [float(score) for score in negative_scores],
            },
        )

        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")
        fig = px.line(
            df,
            x="Date",
            y=["Positive Scores", "Negative Scores"],
            title="Mood score of each entry",
        )
        st.plotly_chart(fig)
