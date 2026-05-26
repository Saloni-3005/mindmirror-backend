import json

def detect_burnout():

    try:
        with open("emotion_history.json", "r") as file:
            history = json.load(file)
    except:
        print("No emotion history found")
        return

    # last 7 records
    last_data = history[-7:]

    stress_count = 0

    for entry in last_data:
        if entry["final"] in ["High Stress", "Moderate Stress"]:
            stress_count += 1

    if stress_count >= 5:
        print("\nAI Insight:")
        print("User stress increasing for several days")
        print("Possible burnout risk detected")

    else:
        print("\nAI Insight:")
        print("No burnout risk detected")