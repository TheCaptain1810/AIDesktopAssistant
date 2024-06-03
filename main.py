import os
import webbrowser
import datetime
import platform
import pyttsx3
import openai
import speech_recognition as sr
import config

chatStr = ""

# Constants for application paths and URLs
MUSIC_PATH = "D:\\Music\\can-you-hear-the-music.mp3"
SITES = [
    ["youtube", "https://www.youtube.com"],
    ["wikipedia", "https://www.wikipedia.com"],
    ["google", "https://www.google.com"],
    ["facebook", "https://www.facebook.com"],
    ["twitter", "https://www.twitter.com"],
    ["instagram", "https://www.instagram.com"],
    ["linkedin", "https://www.linkedin.com"],
    ["reddit", "https://www.reddit.com"],
    ["github", "https://www.github.com"],
    ["amazon", "https://www.amazon.com"],
    ["netflix", "https://www.netflix.com"],
    ["spotify", "https://www.spotify.com"],
    ["news", "https://www.cnn.com"],
    ["email", "https://www.gmail.com"]
]


def chat(queries):
    global chatStr
    chatStr += f"Captain: {queries}\nJarvis: "
    try:
        response_text = generate_response(queries)
        say(response_text)
        chatStr += f"{response_text}\n"
        return response_text
    except Exception as e:
        print(f"Error: {e}")
        return "Some error occurred."


def generate_response(queries):
    openai.api_key = config.apikey
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            say("Sorry, I didn't understand that.")
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Error: {e}")
            return ""


def open_application(app_name):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            if app_name == "facetime":
                os.system("open /System/Applications/FaceTime.app")
            elif app_name == "pass":
                os.system("open /Applications/Passky.app")
            elif app_name == "music":
                os.system(f"open {MUSIC_PATH}")
        elif os_name == "Windows":
            if app_name == "facetime":
                os.system("start ms-settings:privacy-callhistory")
            elif app_name == "pass":
                os.system("start passky")
            elif app_name == "music":
                os.system(f"start {MUSIC_PATH}")
        elif os_name == "Linux":
            if app_name == "facetime":
                os.system("xdg-open /usr/share/applications/org.gnome.Cheese.desktop")
            elif app_name == "pass":
                os.system("xdg-open passky")
            elif app_name == "music":
                os.system(f"xdg-open {MUSIC_PATH}")
    except Exception as e:
        print(f"Error opening {app_name}: {e}")


if __name__ == '__main__':
    print('Welcome to Jarvis AI')
    say("Welcome to Jarvis AI")
    while True:
        query = takeCommand()
        if not query:
            continue

        if query == "shutdown":
            say("Goodbye, sir.")
            break

        if "reset chat" in query:
            chatStr = ""
            say("Chat history reset.")
            continue

        for site in SITES:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}, sir...")
                webbrowser.open(site[1])
                break
        else:
            if "play music" in query:
                open_application("music")
            elif "the time" in query:
                current_time = datetime.datetime.now().strftime("%H:%M")
                say(f"Sir, the time is {current_time}")
            elif "open facetime" in query:
                open_application("facetime")
            elif "open pass" in query:
                open_application("pass")
            else:
                chat(query)
