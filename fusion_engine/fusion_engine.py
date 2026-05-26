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

def fuse_emotions(face_emotion, voice_emotion):
    face_emotion = face_emotion.lower()
    voice_emotion = voice_emotion.lower()
    # High Stress Conditions
    if (face_emotion in ["angry", "fear", "fearful", "disgust"]) and (voice_emotion in ["angry", "fearful"]):
        return "High Stress"

    # Anxiety Condition
    elif (face_emotion == "sad" and voice_emotion in ["fearful", "angry"]):
        return "Anxiety"

    # Sadness
    elif (face_emotion == "sad" and voice_emotion == "sad"):
        return "Sad"

    # Happy State
    elif (face_emotion == "happy" and voice_emotion in ["happy", "calm"]):
        return "Happy"

    # Neutral State
    elif (face_emotion == "neutral" and voice_emotion == "neutral"):
        return "Neutral"

    # Mixed Emotion
    else:
        return "Mixed Emotion"

def fusion_engine(face_emotion, voice_emotion, focus_level, sentiment):

    negative_emotions = ["sad", "angry", "fear", "fearful", "disgust"]

    score = 0

    # Face emotion check
    if face_emotion.lower() in negative_emotions:
        score += 1

    # Voice emotion check
    if voice_emotion.lower() in negative_emotions:
        score += 1

    # Focus level check
    if focus_level.lower() == "low":
        score += 1

    # Sentiment check
    if sentiment.lower() == "negative":
        score += 1

    # Final decision
    if score >= 3:
        return "High Stress"

    elif score == 2:
        return "Moderate Stress"

    else:
        return "Low Stress"


def weighted_fusion(face_emotion, voice_emotion, focus_level, sentiment):
    
    face_score = emotion_scores.get(face_emotion.lower(),1)
    voice_score = emotion_scores.get(voice_emotion.lower(),1)

    focus_score = 3 if focus_level.lower() == "low" else 1
    sentiment_score = 3 if sentiment.lower() == "negative" else 1
    

    # weights
    face_weight = 0.4
    voice_weight = 0.3
    focus_weight = 0.2
    sentiment_weight = 0.1

    final_score = (
        face_score * face_weight +
        voice_score * voice_weight +
        focus_score * focus_weight +
        sentiment_score * sentiment_weight
    )

    # final state
    if final_score >= 2.2:
        return "High Stress"

    elif final_score >= 1.5:
        return "Moderate Stress"

    else:
        return "Low Stress"

def run_fusion(face_emotion, voice_emotion, focus_level, sentiment):

    basic_emotion = fuse_emotions(face_emotion, voice_emotion)

    rule_state = fusion_engine(
        face_emotion,
        voice_emotion,
        focus_level,
        sentiment
    )

    final_state = weighted_fusion(
        face_emotion,
        voice_emotion,
        focus_level,
        sentiment
    )

    return basic_emotion, rule_state, final_state