import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI Emotion Monitoring Dashboard")

emotion_scores = {
    "happy": 0,
    "neutral": 1,
    "calm": 1,
    "surprise": 1,
    "sad": 2,
    "angry": 3,
    "fear": 3,
    "fearful": 3,
    "disgust": 3
}

def load_data():

    try:
        with open("emotion_history.json", "r") as file:
            data = json.load(file)
    except:
        data = []

    return data


data = load_data()

if len(data) == 0:
    st.write("No emotion data available yet.")
else:

    df = pd.DataFrame(data)

    stress_scores = []

    for i in range(len(df)):

        face = df["face"][i].lower()
        voice = df["voice"][i].lower()

        score = emotion_scores.get(face,1) + emotion_scores.get(voice,1)
        stress_scores.append(score)

    df["stress_score"] = stress_scores

    st.subheader("Emotion Data Table")
    st.dataframe(df)

    st.subheader("Stress Trend")

    fig, ax = plt.subplots()
    ax.plot(df["time"], df["stress_score"], marker="o")

    ax.set_xlabel("Time")
    ax.set_ylabel("Stress Score")

    plt.xticks(rotation=45)

    st.pyplot(fig)