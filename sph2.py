import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from googletrans import Translator
import os

def speech_to_text():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Speak something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("Error with the request")
    except OSError:
        print("Microphone not found or not accessible")
    return None

def translate_text(text, target_lang="gu"):
    try:
        translator = Translator()
        translated = translator.translate(text, src="auto", dest=target_lang)  # Auto-detect language
        translated_text = translated.text.encode("utf-8").decode("utf-8")
        print("Translated:", translated_text)
        return translated_text
    except Exception as e:
        print("Translation error:", e)
        return text  # Return original text if translation fails

def text_to_speech(text, use_pyttsx3=False, lang="gu"):
    try:
        if use_pyttsx3:  # Offline option
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        else:  # Online option using gTTS
            tts = gTTS(text, lang=lang)
            tts.save("output.mp3")
            os.system("start output.mp3")  # Use 'mpg321 output.mp3' for Linux/Mac
    except Exception as e:
        print("Speech synthesis error:", e)

if __name__ == "__main__":
    spoken_text = speech_to_text()
    
    if spoken_text:
        while True:  # Keep asking until a valid choice is made
            lang_choice = input("Translate to Gujarati (gu), English (en), or Hindi (hi)? ").strip().lower()

            if lang_choice in ["gu", "en", "hi"]:
                break  # Exit loop when input is valid
            else:
                print("Invalid choice! Please enter 'gu' for Gujarati, 'en' for English, or 'hi' for Hindi.")

        translated_text = translate_text(spoken_text, target_lang=lang_choice)
        text_to_speech(translated_text, use_pyttsx3=False, lang=lang_choice)