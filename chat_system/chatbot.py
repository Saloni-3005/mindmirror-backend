def emotional_chat(emotion):

    if emotion == "sad":
        print("AI: You seem a little sad today.")
        print("AI: Do you want to talk about what happened?")

    elif emotion == "stress":
        print("AI: You seem stressed.")
        print("AI: I'm here to listen. Tell me what's bothering you.")

    elif emotion == "happy":
        print("AI: You look happy today! That's great.")

    else:
        print("AI: How are you feeling today?")


def start_chat():

    while True:

        user_message = input("You: ")

        if user_message.lower() in ["bye", "exit", "quit"]:
            print("AI: Take care! I'm always here if you want to talk.")
            break

        print("AI: Thank you for sharing that with me.")
        print("AI: Sometimes talking about feelings helps reduce stress.")