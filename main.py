# ai_project/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from emotion_project.emotion_detect import detect_emotion_from_image
from voice_analysis.voice_analysis import detect_voice_emotion
from text_analysis.sentiment import analyze_sentiment
from fusion_engine.fusion_engine import run_fusion
from fusion_engine.stress_score import calculate_stress, stress_level
from fusion_engine.consistency_check import check_emotion_consistency
from attention_tracking.attention import detect_attention_from_image
from digital_twin.predictor import predict_future, behavior_pattern
from mental_health_prediction.risk_model import mental_health_risk
from mental_health_prediction.burnout_detector import detect_burnout
from recommendation_system.recommendation import recommend
from auth import get_current_user, supabase
from database import (
    save_emotion, get_emotion_history, get_stress_history,
    save_recommendation, save_prediction,
    get_predictions, get_recommendations
)

# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="MindMirror AI API")

# CORS origins — env var se lo taaki hardcode na karna pade
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request Models ────────────────────────────────────────────────────────────

class AuthRequest(BaseModel):
    email: str
    password: str

class SentimentRequest(BaseModel):
    text: str

class FuseRequest(BaseModel):
    face: str
    voice: str
    focus: str
    sentiment: str
    attention_percent: int = 0

# ── Auth Routes ───────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "MindMirror API running"}

@app.post("/auth/signup")
def signup(body: AuthRequest):
    try:
        supabase.auth.sign_up({
            "email": body.email,
            "password": body.password
        })
        return {"message": "Signup successful, check your email"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login")
def login(body: AuthRequest):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password
        })
        return {
            "access_token": res.session.access_token,
            "user_id": res.user.id
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/auth/logout")
def logout(user=Depends(get_current_user)):
    supabase.auth.sign_out()
    return {"message": "Logged out"}

# ── Scan Routes ───────────────────────────────────────────────────────────────

@app.post("/scan/face")
async def scan_face(file: UploadFile = File(...)):
    image_bytes = await file.read()
    emotion = detect_emotion_from_image(image_bytes)
    return {"face_emotion": emotion}

@app.post("/scan/voice")
async def scan_voice(file: UploadFile = File(...)):
    audio_path = "voice_analysis/live.wav"
    with open(audio_path, "wb") as f:
        f.write(await file.read())
    emotion = detect_voice_emotion()
    return {"voice_emotion": emotion}

@app.post("/scan/sentiment")
def scan_sentiment(body: SentimentRequest):
    sentiment, stress_prob = analyze_sentiment(body.text)
    label = "Negative" if sentiment == "NEGATIVE" else "Positive"
    return {"sentiment": label, "stress_probability": stress_prob}

@app.post("/scan/attention")
async def scan_attention(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = detect_attention_from_image(image_bytes)
    return result

@app.post("/scan/fuse")
def fuse(body: FuseRequest, user=Depends(get_current_user)):
    basic_emotion, rule_state, final_state = run_fusion(
        body.face, body.voice, body.focus, body.sentiment
    )
    score = calculate_stress(body.face, body.voice)
    level = stress_level(score)

    check_emotion_consistency(body.face, body.voice, body.sentiment)

    # ✅ Supabase mein save — saare columns ke saath
    save_emotion(
        user_id=user.id,
        face=body.face,
        voice=body.voice,
        final=final_state,
        stress=score,
        focus=body.focus,
        basic_emotion=basic_emotion,
        rule_state=rule_state,
        stress_level=level,
        sentiment=body.sentiment,
        attention_percent=getattr(body, "attention_percent", 0),
    )

    # ✅ Recommendation save karo
    rec = recommend(final_state, level)
    save_recommendation(
        user_id=user.id,
        emotion=final_state,
        stress_level=level,
        recommendation=rec
    )

    return {
        "basic_emotion": basic_emotion,
        "rule_state": rule_state,
        "final_state": final_state,
        "stress_score": score,
        "stress_level": level,
        "recommendation": rec,
    }

# ── Profile Routes ────────────────────────────────────────────────────────────

@app.get("/profile/history")
def history(user=Depends(get_current_user)):
    data = get_emotion_history(user.id)
    return {"history": data}

@app.get("/profile/stress")
def stress_hist(user=Depends(get_current_user)):
    data = get_stress_history(user.id)
    return {"stress_history": data}

@app.get("/profile/predict")
def predict(user=Depends(get_current_user)):
    try:
        result = predict_future()
        if result:
            save_prediction(
                user_id=user.id,
                stress_risk=result.get("risk", "Low"),
                risk_percent=result.get("risk_percent", 0),
                reason=result.get("reason", ""),
                suggestion=result.get("suggestion", ""),
                best_focus_time=result.get("best_focus_time", "")
            )
        return result or {"message": "Not enough data for prediction"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/profile/burnout")
def burnout(user=Depends(get_current_user)):
    try:
        result = detect_burnout()
        return result or {"message": "Burnout check complete"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/profile/risk")
def risk(user=Depends(get_current_user)):
    try:
        result = mental_health_risk()
        return result or {"message": "Risk check complete"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/profile/recommendations")
def recommendations(user=Depends(get_current_user)):
    data = get_recommendations(user.id)
    return {"recommendations": data}

@app.get("/profile/predictions")
def predictions(user=Depends(get_current_user)):
    data = get_predictions(user.id)
    return {"predictions": data}