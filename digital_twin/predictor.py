import json

PROFILE_FILE = "digital_twin/user_profile.json"


def predict_future():

    try:
        with open(PROFILE_FILE, "r") as file:
            data = json.load(file)
    except:
        print("No data for prediction.")
        return

    stress_history = data["stress_history"][-20:]
    focus_history = data["focus_history"][-20:]

    if len(stress_history) < 3:
        print("Need at least 3 sessions for prediction.")
        return

    # Average stress
    total_stress = sum(item["stress"] for item in stress_history)
    avg_stress = total_stress / len(stress_history)

    # Risk %
    risk_percent = int((avg_stress / 5) * 100)

    # Risk label
    if avg_stress > 4:
        risk = "High"
    elif avg_stress > 2:
        risk = "Moderate"
    else:
        risk = "Low"

    # Last 3 sessions trend
    last_three = [item["stress"] for item in stress_history[-3:]]

    if last_three[0] < last_three[1] < last_three[2]:
        reason = "Stress increased 3 sessions continuously"
    elif last_three[0] > last_three[1] > last_three[2]:
        reason = "Stress improving in recent sessions"
    else:
        reason = "Stress fluctuating recently"

    # Suggestion
    if risk == "High":
        suggestion = "Take regular breaks tomorrow."
    elif risk == "Moderate":
        suggestion = "Maintain balance and rest properly."
    else:
        suggestion = "Keep up your healthy routine."

    # Best focus time
    best_focus = max(focus_history, key=lambda x: x["focus"])

    print("\nAI Prediction System")
    print(f"Tomorrow Stress Risk: {risk} ({risk_percent}%)")
    print("Reason:", reason)
    print("Suggestion:", suggestion)
    print("Best Focus Time:", best_focus["time"])




def behavior_pattern():

    try:
        with open(PROFILE_FILE, "r") as file:
            data = json.load(file)
    except:
        print("No behavior data found.")
        return

    stress_history = data["stress_history"][-20:]
    focus_history = data["focus_history"][-20:]

    if not stress_history:
        print("Not enough data for behavior analysis.")
        return

    # Find highest stress
    highest_stress = max(stress_history, key=lambda x: x["stress"])

    # Find highest focus
    highest_focus = max(focus_history, key=lambda x: x["focus"])

    print("\nBehavior Pattern Analysis")
    print("Most Stress Time:", highest_stress["time"])
    print("Most Focused Time:", highest_focus["time"])

    if highest_stress["stress"] > 4:
        print("Insight: High pressure usually occurs at this time.")