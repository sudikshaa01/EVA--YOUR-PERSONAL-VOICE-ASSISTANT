import pyttsx3, speech_recognition as sr, random, webbrowser, datetime, os, requests
import pyautogui, wikipedia, pywhatkit as pwk
from plyer import notification
from translate import Translator
import tkinter as tk
from tkinter import Canvas, Frame
import threading

engine = pyttsx3.init()
engine.setProperty('voice', pyttsx3.init().getProperty('voices')[1].id)
engine.setProperty("rate", 170)

def speak(audio): engine.say(audio); engine.runAndWait()
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening please tell what you want me to do for you...")
        audio = r.listen(source)
    try: return r.recognize_google(audio, language='en-in').lower()
    except: speak("Try again."); return ""

# --- FEATURES ---
def main_process():
    request = command()
    if "hello" in request: speak("Welcome, how can I help you.")
    elif "play music" in request:
        speak("Playing music")
        webbrowser.open(random.choice([
            "https://youtu.be/BSJa1UytM8w?si=JDAHCxbSNgSOU0bd",
            "https://youtu.be/-2RAq5o5pwc?si=RuFfNfg_53URuv8R"
        ]))
    elif "say time" in request: speak("Time is " + datetime.datetime.now().strftime("%H:%M"))
    elif "say date" in request: speak("Date is " + datetime.datetime.now().strftime("%d %B %Y"))
    elif "new task" in request:
        task = request.replace("new task", "").strip()
        with open("todo.txt", "a") as f: f.write(task + "\n")
        speak("Task added")
    elif "speak task" in request:
        with open("todo.txt", "r") as f: speak("Tasks are: " + f.read())
    elif "show work" in request:
        with open("todo.txt", "r") as f: notification.notify(title="Today's Work", message=f.read())
    elif "open youtube" in request: webbrowser.open("https://www.youtube.com")
    elif "open" in request:
        app = request.replace("open", "").strip()
        pyautogui.press("super")
        pyautogui.write(app)
        pyautogui.sleep(2)
        pyautogui.press("enter")
    elif "wikipedia" in request:
        topic = request.replace("search wikipedia", "").strip()
        speak(wikipedia.summary(topic, sentences=2))
    elif "search google" in request:
        query = request.replace("search google", "").strip()
        webbrowser.open("https911234567890://www.google.com/search?q=" + query)
    elif "send whatsapp" in request:
        pwk.sendwhatmsg("+", "Hello", 20, 46)
    elif "translate" in request: translate_text()
    elif "where am i" in request or "my location" in request: get_location()
    elif "system control" in request: system_control()
    elif "generate image" in request: generate_image_from_voice()

def translate_text():
    speak("What should I translate?")
    text = command()
    speak("To which language?")
    lang = command().lower()
    lang_dict = {
        "hindi": "hi", "spanish": "es", "french": "fr", "german": "de",
        "tamil": "ta", "telugu": "te", "english": "en", "japanese": "ja", "korean": "ko"
    }
    if lang not in lang_dict: speak("Language not supported."); return
    translated = Translator(to_lang=lang_dict[lang]).translate(text)
    speak(f"In {lang}, it means: {translated}")

def get_location():
    try:
        data = requests.get("https://ipinfo.io").json()
        speak(f"You are in {data['city']}, {data['region']}, {data['country']}")
    except: speak("Couldn't get location")

def generate_image_from_voice():
    speak("What should I generate?")
    prompt = command()
    if prompt:
        webbrowser.open(f"https://www.craiyon.com/?prompt={prompt.replace(' ', '%20')}")
        speak("Opening image prompt.")

def system_control():
    speak("Shutdown, restart or sleep?")
    action = command()
    if "shutdown" in action: os.system("shutdown /s /t 1")
    elif "restart" in action: os.system("shutdown /r /t 1")
    elif "sleep" in action: os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else: speak("Command not recognized")


# --- GUI ---
root = tk.Tk()
root.title("Jarvis Assistant")
root.geometry("480x700")
root.configure(bg="#121212")

canvas = Canvas(root, bg="#121212", highlightthickness=0)
scroll = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll.pack(side="right", fill="y")

frame = Frame(canvas, bg="#121212")
canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.pack(fill="both", expand=True)
canvas.configure(yscrollcommand=scroll.set)

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

frame.bind("<Configure>", on_configure)

# --- Styling ---
def section(title):
    tk.Label(frame, text=title, font=("Arial", 14, "bold"), fg="#00BFFF", bg="#121212").pack(anchor="w", padx=16, pady=(20, 10))

def add_button(text, func):
    btn = tk.Button(frame, text="  " + text, font=("Arial", 12), fg="white",
                    bg="#1e1e1e", width=40, height=2, relief="flat",
                    command=lambda: threading.Thread(target=func).start())
    btn.pack(pady=6, padx=20)

# --- Title ---
tk.Label(frame, text="🤖 Jarvis - Your Smart Assistant", font=("Arial", 18, "bold"),
         fg="white", bg="#121212").pack(pady=20)

# --- Sections ---
section("🎤 Voice & Assistant")
add_button("🎙 Start Listening", main_process)

section("🌍 Web Actions")
add_button("🌐 Open Google", lambda: webbrowser.open("https://www.google.com"))
add_button("📖 Search Wikipedia", lambda: speak(wikipedia.summary(command(), sentences=2)))
add_button("📺 Open YouTube", lambda: webbrowser.open("https://www.youtube.com"))


section("🎶 Entertainment")
add_button("🎵 Play Music", lambda: webbrowser.open(random.choice([
            "https://youtu.be/BSJa1UytM8w?si=JDAHCxbSNgSOU0bd",
            "https://youtu.be/-2RAq5o5pwc?si=RuFfNfg_53URuv8R"
        ])))




section("🧰 Utilities")
add_button("🔤 Translate Text", translate_text)
add_button("📍 Get Location", get_location)
add_button("🖼 Generate Image", generate_image_from_voice)
add_button("📂 Open Folder", lambda: os.startfile(os.getcwd()))
add_button("💬 Send WhatsApp", lambda: pwk.sendwhatmsg("+917009298501", "Hello", 20, 46))

section("⚙ System & Tasks")
add_button("⚙ System Control", system_control)
add_button("📝 Speak Tasks", lambda: speak(open("todo.txt").read()))
add_button("🕒 Say Time", lambda: speak("Time: " + datetime.datetime.now().strftime("%H:%M")))
add_button("📅 Say Date", lambda: speak("Date: " + datetime.datetime.now().strftime("%d %B %Y")))


root.mainloop()
