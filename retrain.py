import numpy as np
import librosa
import os
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

print("NumPy version:", np.__version__)

dataset_path = "/app/voice_analysis/dataset"

features, labels = [], []

if os.path.exists(dataset_path):
    for actor in os.listdir(dataset_path):
        folder = os.path.join(dataset_path, actor)
        if not os.path.isdir(folder): continue
        for f in os.listdir(folder):
            if f.endswith(".wav"):
                parts = f.split("-")
                if len(parts) > 2:
                    try:
                        audio, sr = librosa.load(os.path.join(folder, f), duration=3, offset=0.5)
                        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
                        features.append(np.mean(mfcc.T, axis=0))
                        labels.append(parts[2])
                    except:
                        pass

# Dataset nahi hai toh dummy model
if len(features) < 10:
    print("Dataset nahi mila — dummy model bana raha hai")
    X = np.random.rand(200, 40).astype(np.float32)
    y = np.random.choice(['01','02','03','04','05','06','07','08'], 200)
else:
    X = np.array(features)
    y = np.array(labels)

scaler = StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=100)
model.fit(X_train, y_train)
print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, "/app/voice_analysis/voice_emotion_model.pkl")
joblib.dump(scaler, "/app/voice_analysis/scaler.pkl")
print("✅ Models saved!")