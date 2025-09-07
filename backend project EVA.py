# --- IMPORTS ---
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import pyautogui
import wikipedia
import pywhatkit as pwk
import user_config
import os
import requests
import pytesseract
from translate import Translator
import time  
from datetime import datetime



# --- INIT ENGINE ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 170)




def speak(audio):
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()
    engine.stop()  # Prevent voice clipping



# --- VOICE COMMAND FUNCTION ---
def command():
    content = ""
    while content == "":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            content = r.recognize_google(audio, language='en-in')
            print("You said:", content)
        except Exception:
            print("Please try again...")
    return content



# --- TRANLATOR ---

def translate_text():
    try:
        print("\n=== DEBUG: Starting translation ===")
        
        # Step 1: Get text to translate
        speak("What would you like me to translate?")
        print("DEBUG: Listening for text...")
        text = command()
        print(f"DEBUG: Heard text: {text}")
        
        if not text:
            speak("I didn't hear anything to translate.")
            return

        # Step 2: Get target language
        speak("Which language? Say like Hindi, Spanish, French etc.")
        print("DEBUG: Listening for language...")
        lang_name = command().lower()
        print(f"DEBUG: Heard language: {lang_name}")
        
        lang_dict = {
            "hindi": "hi", "spanish": "es", "french": "fr",
            "german": "de", "tamil": "ta", "telugu": "te",
            "english": "en", "japanese": "ja", "korean": "ko"
        }

        if lang_name not in lang_dict:
            error_msg = f"Sorry, I don't support {lang_name}. Try: {', '.join(lang_dict.keys())}"
            print(f"DEBUG: {error_msg}")
            speak(error_msg)


            return

        # Step 3: Perform translation
        print(f"DEBUG: Attempting translation to {lang_dict[lang_name]}...")
        speak(f"Translating to {lang_name}, please wait...")
        translator = Translator(to_lang=lang_dict[lang_name])
        translated = translator.translate(text)
        
        print(f"DEBUG: Translation successful!")
        print(f"Original: {text}")
        print(f"Translated: {translated}")

        # Step 4: Speak results
        engine.setProperty("rate", 150)
        speak(f"In {lang_name}, this means: {translated}")
        engine.setProperty("rate", 170)
        
        print("=== DEBUG: Translation complete ===\n")
        
    except Exception as e:
        error_msg = f"Translation failed: {str(e)}"
        print(f"DEBUG ERROR: {error_msg}")
        speak("Sorry, my translator malfunctioned. Please try again.")




# --- LOCATION DETECTION ---
def get_location():
    ip_info = requests.get('https://ipinfo.io').json()
    city = ip_info.get("city")
    region = ip_info.get("region")
    country = ip_info.get("country")
    speak(f"You are in {city}, {region}, {country}.")




# --- IMAGE GENERATION ---

def generate_image_from_voice():
    try:
        speak("What image would you like me to generate?")
        prompt = command()
        if not prompt:
            speak("I didn't hear anything.")
            return
        
        speak(f"Generating an image of {prompt}. Please wait, opening in browser.")
        search_url = f"https://www.craiyon.com/?prompt={prompt.replace(' ', '%20')}"
        webbrowser.open(search_url)
    except Exception as e:
        print(f"Image generation failed: {e}")
        speak("Sorry, something went wrong while generating the image.")



# --- SYSTEM CONTROL ---
def system_control():
    speak("What system action should I perform? Shutdown, restart or sleep?")
    action = command().lower()
    if "shutdown" in action:
        speak("Shutting down now.")
        os.system("shutdown /s /t 1")
    elif "restart" in action:
        speak("Restarting system.")
        os.system("shutdown /r /t 1")
    elif "sleep" in action:
        speak("Putting system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        speak("Action not recognized.")


# --- MAIN PROCESS ---
def main_process():
    while True:
        request = command().lower()

        if "hello" in request:
            speak("Welcome, how can I help you.")
        elif "play music" in request:
            speak("Playing music")
            song = random.choice([
                "https://www.youtube.com/watch?v=1pWa72yWfYE&list=RD1pWa72yWfYE&start_radio=1",
                "https://www.youtube.com/watch?v=mN3ioy2oipA&list=RDmN3ioy2oipA&start_radio=1",
                "https://www.youtube.com/watch?v=LaEurVYTXGk&list=RDLaEurVYTXGk&start_radio=1"
            ])
            webbrowser.open(song)
        elif "say time" in request:
            now_time = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + now_time)
        elif "say date" in request:
            now_date = datetime.datetime.now().strftime("%d:%m")
            speak("Current date is " + now_date)
        elif "open youtube" in request:
            webbrowser.open("www.youtube.com")
        elif "open" in request:
            query = request.replace("open", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(2)
            pyautogui.press("enter")
        elif "wikipedia" in request:
            request = request.replace("eva ", "").replace("search wikipedia ", "")
            result = wikipedia.summary(request, sentences=2)
            speak(result)
        elif "search google" in request:
            request = request.replace("eva ", "").replace("search google ", "")
            result1=webbrowser.open("https://www.google.com/search?q=" + request)
            speak(result1)
# from datetime import datetime
        elif "send whatsapp" in request:
            now=datetime.now()
            pwk.sendwhatmsg("+911234567890", "Hello, how are you",now.hour,now.minute +2)

        # elif "send whatsapp" in request:
        #     pwk.sendwhatmsg("+911234567890", "Hello, how are you", 7, 18, 30)
        elif "translate" in request:
            translate_text()
        elif "where am i" in request or "my location" in request:
            get_location()
        elif "system control" in request:
            system_control()
        elif "generate image" in request or "create image" in request:
            generate_image_from_voice()

        

# --- MAIN ---
main_process()