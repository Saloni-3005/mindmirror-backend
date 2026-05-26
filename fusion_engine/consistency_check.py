def check_emotion_consistency(face, voice, sentiment):

    print("\nEmotion Consistency Check")

    negative_signals = 0
    negative_emotions = ["sad", "angry", "fear", "disgust"]

    # face emotion
    if face.lower() in negative_emotions:
        negative_signals += 1

    # voice emotion
    if voice.lower() in negative_emotions:
        negative_signals += 1

    # text sentiment
    if sentiment == "Negative":
        negative_signals += 1

    # distress detection
    if negative_signals >= 2:
        print("Possible emotional distress detected")

    # hiding emotion detection
    if face.lower() == "happy" and sentiment == "Negative":
        print("User hiding emotions detected")

    # mismatch detection
    face_negative = face.lower() in negative_emotions
    voice_negative = voice.lower() in negative_emotions
    text_negative = sentiment == "Negative"

    if (face_negative != voice_negative) or (face_negative != text_negative):
        print("Emotion Mismatch Detected")
        print("User may be hiding emotions")

    else:
        print("Emotions are consistent")