import speech_recognition as sr
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

def listen_to_user():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening for input...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("🗣️ You said:", text)
        return text
    except sr.UnknownValueError:
        print("⚠️ Sorry, I didn't catch that.")
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("⚠️ Network error.")
        speak("There was a network error.")
        return ""

def speak(text):
    print("🤖 Speaking:", text)
    engine.say(text)
    engine.runAndWait()
