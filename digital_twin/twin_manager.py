import json
import datetime

PROFILE_FILE = "digital_twin/user_profile.json"


def update_profile(emotion, stress, focus):

    current_time = datetime.datetime.now().strftime("%H:%M")

    try:
        with open(PROFILE_FILE, "r") as file:
            data = json.load(file)
    except:
        data = {
            "emotion_history": [],
            "stress_history": [],
            "focus_history": []
        }

    data["emotion_history"].append({
        "time": current_time,
        "emotion": emotion
    })

    data["stress_history"].append({
        "time": current_time,
        "stress": stress
    })

    data["focus_history"].append({
        "time": current_time,
        "focus": focus
    })
    # Keep only latest 50 records
    data["emotion_history"] = data["emotion_history"][-50:]
    data["stress_history"] = data["stress_history"][-50:]
    data["focus_history"] = data["focus_history"][-50:]

    with open(PROFILE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def analyze_profile():

    with open(PROFILE_FILE, "r") as file:
        data = json.load(file)

    if not data["stress_history"]:
        print("No profile data yet.")
        return

    # Highest stress
    max_stress = max(data["stress_history"], key=lambda x: x["stress"])

    # Highest focus
    max_focus = max(data["focus_history"], key=lambda x: x["focus"])

    print("\nDigital Twin Analysis")
    print("Stress highest:", max_stress["time"])
    print("Focus highest:", max_focus["time"])