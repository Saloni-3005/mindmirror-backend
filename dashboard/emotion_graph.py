import json
import matplotlib.pyplot as plt

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

def show_emotion_graph():

    try:
        with open("emotion_history.json", "r") as file:
            history = json.load(file)
    except:
        print("No emotion history found.")
        return

    times = []
    stress_scores = []

    for entry in history:

        face = entry["face"].lower()
        voice = entry["voice"].lower()

        face_score = emotion_scores.get(face, 1)
        voice_score = emotion_scores.get(voice, 1)

        total_score = face_score + voice_score

        stress_scores.append(total_score)
        times.append(entry["time"])

    plt.figure(figsize=(8,4))
    plt.plot(times, stress_scores, marker='o')

    plt.title("Emotion / Stress History")
    plt.xlabel("Time")
    plt.ylabel("Stress Score")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()