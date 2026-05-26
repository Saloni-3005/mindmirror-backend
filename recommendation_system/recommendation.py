def recommend(emotion, stress_level):

    # High stress recommendations
    if stress_level == "High Stress":
        return "Take a 5-minute break, drink water, and try deep breathing."

    # Moderate stress recommendations
    elif stress_level == "Moderate Stress":
        return "Relax for a moment, stretch your body, or listen to calm music."

    # Low stress
    elif stress_level == "Low Stress":
        return "You are doing well. Keep going!"

    # Emotion-based suggestions
    if emotion == "sad":
        return "Talk to a friend or listen to your favorite music."

    elif emotion == "angry":
        return "Take deep breaths and step away from the screen for a few minutes."

    elif emotion == "happy":
        return "Great mood! Keep doing what you are doing."

    return "Stay calm and maintain a balanced routine."