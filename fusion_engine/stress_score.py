emotion_scores = {
    "happy": 0,
    "neutral": 1,
    "calm": 1,
    "sad": 2,
    "surprise": 1,
    "surprised": 1,
    "angry": 3,
    "fear": 3,
    "fearful": 3,
    "disgust": 3
}
def calculate_stress(face_emotion, voice_emotion):

    face_score = emotion_scores.get(face_emotion.lower(), 1)
    voice_score = emotion_scores.get(voice_emotion.lower(), 1)

    total_score = face_score + voice_score

    return total_score

def stress_level(score):

    if score <= 1:
        return "No Stress"
    elif score <= 2:
        return "Low Stress"

    elif score <= 4:
        return "Moderate Stress"

    else:
        return "High Stress"