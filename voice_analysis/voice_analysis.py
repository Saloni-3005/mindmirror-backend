import numpy as np
import librosa
import os
import joblib  # pickle ki jagah

# Line 10 change karo:
BASE_DIR = os.path.dirname(__file__)  
model = joblib.load(os.path.join(BASE_DIR, "voice_emotion_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
# BASE_DIR = os.path.dirname(__file__)

# # model load
# with open(os.path.join(BASE_DIR,"voice_emotion_model.pkl"),"rb") as f:
#     model = pickle.load(f)

# # scaler load
# with open(os.path.join(BASE_DIR,"scaler.pkl"),"rb") as f:
#     scaler = pickle.load(f)

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

    audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')

    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)

    mfccs_processed = np.mean(mfccs.T, axis=0)

    return mfccs_processed


def detect_voice_emotion():

    audio_file = os.path.join(BASE_DIR,"live.wav")

    mfcc = extract_features(audio_file)

    mfcc = mfcc.reshape(1,-1)

    mfcc = scaler.transform(mfcc)

    prediction = model.predict(mfcc)

    emotion = emotion_dict[prediction[0]]

    print("Voice Emotion:", emotion)

    return emotion