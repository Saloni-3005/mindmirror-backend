# import numpy as np
# import librosa
# import os
# import joblib  # pickle ki jagah

# # Line 10 change karo:
# BASE_DIR = os.path.dirname(__file__)  
# model = joblib.load(os.path.join(BASE_DIR, "voice_emotion_model.pkl"))
# scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# emotion_dict = {
#     '01': 'neutral',
#     '02': 'calm',
#     '03': 'happy',
#     '04': 'sad',
#     '05': 'angry',
#     '06': 'fearful',
#     '07': 'disgust',
#     '08': 'surprised'
# }

# def extract_features(file_name):

#     audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')

#     mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)

#     mfccs_processed = np.mean(mfccs.T, axis=0)

#     return mfccs_processed


# def detect_voice_emotion():

#     audio_file = os.path.join(BASE_DIR,"live.wav")

#     mfcc = extract_features(audio_file)

#     mfcc = mfcc.reshape(1,-1)

#     mfcc = scaler.transform(mfcc)

#     prediction = model.predict(mfcc)

#     emotion = emotion_dict[prediction[0]]

#     print("Voice Emotion:", emotion)

#     return emotion

import numpy as np
import librosa
import os
import joblib

BASE_DIR = os.path.dirname(__file__)
model = joblib.load(os.path.join(BASE_DIR, "voice_emotion_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

emotion_dict = {
    '01': 'neutral',
    '02': 'calm',
    '03': 'happy',
    '04': 'sad',
    '05': 'angry',
    '06': 'fearful',
    '07': 'disgust',
    '08': 'surprised'
}

def extract_features(file_name):
    print(f"[VOICE] Step A: loading audio file {file_name}", flush=True)
    audio, sample_rate = librosa.load(file_name, sr=22050, res_type='kaiser_fast')
    print(f"[VOICE] Step B: audio loaded, len={len(audio)}, sr={sample_rate}", flush=True)

    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    print(f"[VOICE] Step C: mfcc extracted, shape={mfccs.shape}", flush=True)

    mfccs_processed = np.mean(mfccs.T, axis=0)
    print(f"[VOICE] Step D: mfcc averaged", flush=True)

    return mfccs_processed


def detect_voice_emotion():
    audio_file = os.path.join(BASE_DIR, "live.wav")
    print(f"[VOICE] Starting detection for {audio_file}", flush=True)

    mfcc = extract_features(audio_file)

    mfcc = mfcc.reshape(1, -1)
    print(f"[VOICE] Step E: reshaped", flush=True)

    mfcc = scaler.transform(mfcc)
    print(f"[VOICE] Step F: scaled", flush=True)

    prediction = model.predict(mfcc)
    print(f"[VOICE] Step G: predicted = {prediction}", flush=True)

    pred_label = str(prediction[0])
    emotion = emotion_dict.get(pred_label, "unknown")
    print(f"[VOICE] Step H: final emotion = {emotion}", flush=True)

    return emotion