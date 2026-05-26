import json
import datetime
import time
from emotion_project.emotion_detect import detect_face_emotion
from voice_analysis.voice_analysis import detect_voice_emotion
from text_analysis.sentiment import analyze_sentiment
from text_analysis.speech import speech_to_text
from fusion_engine.fusion_engine import fuse_emotions, fusion_engine, weighted_fusion
from fusion_engine.stress_score import calculate_stress, stress_level
from fusion_engine.consistency_check import check_emotion_consistency
from recommendation_system.recommendation import recommend
from chat_system.chatbot import emotional_chat, start_chat
from attention_tracking.attention import check_attention
from dashboard.emotion_graph import show_emotion_graph
from digital_twin.twin_manager import update_profile, analyze_profile
from digital_twin.predictor import predict_future, behavior_pattern
from mental_health_prediction.risk_model import mental_health_risk
from mental_health_prediction.burnout_detector import detect_burnout


def save_emotion(face_emotion, voice_emotion, final_emotion):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    data = {"face": face_emotion, "voice": voice_emotion,
        "time": current_time, "final": final_emotion}

    try:
        with open("emotion_history.json", "r") as file:
            history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    history.append(data)

    with open("emotion_history.json", "w") as file:
        json.dump(history, file, indent=4)


def run_system():

    print("Starting Emotion Detection System...")

    face_emotion = detect_face_emotion()
    print("Face Emotion:", face_emotion)

    print("Starting Voice Detection System...")
    voice_emotion = detect_voice_emotion()
    print("Voice Emotion Detected:", voice_emotion)

    final_emotion = fuse_emotions(face_emotion, voice_emotion)

    user_text = input("\nHow are you feeling today? ")
    sentiment, stress_prob = analyze_sentiment(user_text)

    sentiment_state = "Negative" if sentiment == "NEGATIVE" else "Positive"
    print("\nStarting Voice Conversation Mode...")

    voice_text = speech_to_text()

    if voice_text:
     sentiment, stress_prob = analyze_sentiment(voice_text)
     sentiment_state = "Negative" if sentiment == "NEGATIVE" else "Positive"


    print("\nFinal Results")
    print("Face Emotion:", face_emotion)
    print("Voice Emotion:", voice_emotion)
    print("Basic Emotion:", final_emotion)

    focus_level = "Low"
    sentiment = sentiment_state

    rule_state = fusion_engine(face_emotion, voice_emotion, focus_level, sentiment)
    print("Rule Based State:", rule_state)

    final_state = weighted_fusion(
       face_emotion,
       voice_emotion,
       focus_level,
       sentiment
    )

    print("Weighted Fusion State:", final_state)

    check_emotion_consistency(
    face_emotion,
    voice_emotion,
    sentiment
)

    # Save emotion history
    save_emotion(face_emotion, voice_emotion, final_state)

    stress_score = calculate_stress(face_emotion, voice_emotion)

    print("Stress Score:", stress_score)
    
    
    print("Checking User Attention...")
    focus_level = check_attention()

    focus_score = 1 if focus_level == "Low" else 3

    update_profile(
      final_state,
      stress_score,
      focus_score
   )
    level = stress_level(stress_score)
    print("Stress Level:", level)
    recommendation = recommend(final_state, level)

    print("Recommendation:", recommendation)
    emotional_chat(final_state)
    start_chat()

    print("\nShowing Emotion History Graph...")
    show_emotion_graph()

    analyze_profile()

    print("\nRunning AI Prediction...")
    predict_future()
    print("\nRunning Behavior Analysis...")
    behavior_pattern()

    print("\nChecking Mental Health Risk...")
    mental_health_risk()

    print("\nChecking Burnout Risk...")
    detect_burnout()


if __name__ == "__main__":

    while True:

        run_system()

        again = input("\nRun system again? (yes/no): ").strip().lower()

        if again != "yes":
            print("Goodbye.")
            break