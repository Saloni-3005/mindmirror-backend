# retrain.py
import numpy as np
import librosa
import os
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

print("NumPy version:", np.__version__)

dataset_path = "voice_analysis/dataset"
os.makedirs(dataset_path, exist_ok=True)

# Agar dataset nahi hai toh simple dummy model banao
X = np.random.rand(100, 40).astype(np.float32)
y = np.random.choice(['01','02','03','04','05','06','07','08'], 100)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = MLPClassifier(hidden_layer_sizes=(300,200,100), max_iter=10)
model.fit(X_scaled, y)

joblib.dump(model, "voice_analysis/voice_emotion_model.pkl")
joblib.dump(scaler, "voice_analysis/scaler.pkl")
print("✅ Models saved!")