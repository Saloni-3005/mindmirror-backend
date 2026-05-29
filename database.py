from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_emotion(user_id: str, face: str, voice: str, final: str,
                 stress: int, focus: str, basic_emotion: str = "",
                 rule_state: str = "", stress_level: str = "",
                 sentiment: str = "", attention_percent: int = 0):
    try:
        supabase.table("emotion_history").insert({
            "user_id": user_id,
            "face_emotion": face,
            "voice_emotion": voice,
            "final_state": final,
            "stress_score": stress,
            "focus_level": focus,
            "basic_emotion": basic_emotion,
            "rule_state": rule_state,
            "stress_level": stress_level,
            "sentiment": sentiment,
            "attention_percent": attention_percent
        }).execute()

        supabase.table("stress_history").insert({
            "user_id": user_id,
            "stress": stress
        }).execute()

        focus_score = 3 if focus == "High" else 2 if focus == "Medium" else 1
        supabase.table("focus_history").insert({
            "user_id": user_id,
            "focus": focus_score
        }).execute()

    except Exception as e:
        print(f"Database save error: {e}")


def get_emotion_history(user_id: str):
    try:
        result = supabase.table("emotion_history")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("recorded_at", desc=True)\
            .limit(50)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Database fetch error: {e}")
        return []


def get_stress_history(user_id: str):
    try:
        result = supabase.table("stress_history")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("recorded_at", desc=True)\
            .limit(20)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Database fetch error: {e}")
        return []


def save_recommendation(user_id: str, emotion: str, stress_level: str, recommendation: str):
    try:
        supabase.table("recommendations").insert({
            "user_id": user_id,
            "emotion": emotion,
            "stress_level": stress_level,
            "recommendation": recommendation
        }).execute()
    except Exception as e:
        print(f"Recommendation save error: {e}")


def save_prediction(user_id: str, stress_risk: str, risk_percent: int,
                    reason: str, suggestion: str, best_focus_time: str):
    try:
        supabase.table("predictions").insert({
            "user_id": user_id,
            "stress_risk": stress_risk,
            "risk_percent": risk_percent,
            "reason": reason,
            "suggestion": suggestion,
            "best_focus_time": best_focus_time
        }).execute()
    except Exception as e:
        print(f"Prediction save error: {e}")


def get_predictions(user_id: str):
    try:
        result = supabase.table("predictions")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(10)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Predictions fetch error: {e}")
        return []


def get_recommendations(user_id: str):
    try:
        result = supabase.table("recommendations")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(5)\
            .execute()
        return result.data
    except Exception as e:
        print(f"Recommendations fetch error: {e}")
        return []