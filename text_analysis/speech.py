import speech_recognition as sr

def speech_to_text():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text

    except:
        print("Speech not understood")
        return ""