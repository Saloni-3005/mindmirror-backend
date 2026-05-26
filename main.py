# ai_project/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, datetime

from emotion_project.emotion_detect import detect_emotion_from_image
from voice_analysis.voice_analysis import detect_voice_emotion
from text_analysis.sentiment import analyze_sentiment
from fusion_engine.fusion_engine import run_fusion
from fusion_engine.stress_score import calculate_stress, stress_level
from fusion_engine.consistency_check import check_emotion_consistency
from attention_tracking.attention import detect_attention_from_image
from digital_twin.twin_manager import update_profile, analyze_profile
from digital_twin.predictor import predict_future, behavior_pattern
from mental_health_prediction.risk_model import mental_health_risk
from mental_health_prediction.burnout_detector import detect_burnout

app = FastAPI(title="MindMirror AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production mein apna Cloudflare domain dalna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request Models ────────────────────────────────────────────────────────────

class SentimentRequest(BaseModel):
    text: str

class FuseRequest(BaseModel):
    face: str
    voice: str
    focus: str
    sentiment: str


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "MindMirror API running"}


# 1. Face emotion — frontend webcam frame bhejega
@app.post("/scan/face")
async def scan_face(file: UploadFile = File(...)):
    image_bytes = await file.read()
    emotion = detect_emotion_from_image(image_bytes)
    return {"face_emotion": emotion}


# 2. Voice emotion — frontend audio file bhejega
@app.post("/scan/voice")
async def scan_voice(file: UploadFile = File(...)):
    audio_path = "voice_analysis/live.wav"
    with open(audio_path, "wb") as f:
        f.write(await file.read())
    emotion = detect_voice_emotion()
    return {"voice_emotion": emotion}


# 3. Text sentiment
@app.post("/scan/sentiment")
def scan_sentiment(body: SentimentRequest):
    sentiment, stress_prob = analyze_sentiment(body.text)
    label = "Negative" if sentiment == "NEGATIVE" else "Positive"
    return {"sentiment": label, "stress_probability": stress_prob}


# 4. Attention — frontend webcam frame bhejega
@app.post("/scan/attention")
async def scan_attention(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = detect_attention_from_image(image_bytes)
    return result


# 5. Fusion — sab results combine karo
@app.post("/scan/fuse")
def fuse(body: FuseRequest):
    basic_emotion, rule_state, final_state = run_fusion(
        body.face, body.voice, body.focus, body.sentiment
    )
    score = calculate_stress(body.face, body.voice)
    level = stress_level(score)

    check_emotion_consistency(body.face, body.voice, body.sentiment)

    focus_score = 3 if body.focus == "High" else 2 if body.focus == "Medium" else 1
    update_profile(final_state, score, focus_score)

    # emotion_history.json save karo
    _save_emotion(body.face, body.voice, final_state)

    return {
        "basic_emotion": basic_emotion,
        "rule_state": rule_state,
        "final_state": final_state,
        "stress_score": score,
        "stress_level": level,
    }


# 6. Profile & Predictions
@app.get("/profile/predict")
def predict():
    try:
        result = predict_future()
        return result or {"message": "Prediction complete"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/profile/burnout")
def burnout():
    try:
        result = detect_burnout()
        return result or {"message": "Burnout check complete"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/profile/analyze")
def analyze():
    try:
        result = analyze_profile()
        return result or {"message": "Analysis complete"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/profile/risk")
def risk():
    try:
        result = mental_health_risk()
        return result or {"message": "Risk check complete"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/profile/history")
def history():
    try:
        with open("emotion_history.json", "r") as f:
            data = json.load(f)
        return {"history": data}
    except:
        return {"history": []}


# ─── Helper ───────────────────────────────────────────────────────────────────

def _save_emotion(face: str, voice: str, final: str):
    entry = {
        "face": face,
        "voice": voice,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "final": final
    }
    try:
        with open("emotion_history.json", "r") as f:
            history = json.load(f)
    except:
        history = []
    history.append(entry)
    with open("emotion_history.json", "w") as f:
        json.dump(history, f, indent=4)