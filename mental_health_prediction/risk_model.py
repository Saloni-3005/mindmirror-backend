import json

PROFILE_FILE = "digital_twin/user_profile.json"


def mental_health_risk():

    try:
        with open(PROFILE_FILE, "r") as file:
            data = json.load(file)
    except:
        print("No data available.")
        return

    stress_history = data["stress_history"]

    if len(stress_history) < 7:
        print("Need at least 7 days of mood history for reliable prediction.")
        return

    # last 7 entries
    last_7 = stress_history[-7:]

    stresses = [item["stress"] for item in last_7]

    increasing = all(x < y for x, y in zip(stresses, stresses[1:]))

    if increasing:
        risk = "High"

    elif max(stresses) > 4:
        risk = "Moderate"

    else:
        risk = "Low"

    print("\nMental Health Prediction")
    print("Mental Health Risk:", risk)
    