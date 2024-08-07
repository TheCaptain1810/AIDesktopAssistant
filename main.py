import os
import webbrowser
import datetime
import platform
import pyttsx3
import speech_recognition as sr
import json
import config
from groq import Groq

# Constants
MUSIC_PATH = "D:\\Music\\can-you-hear-the-music.mp3"
COMMANDS_FILE = 'commands.json'
CHAT_RESET_CMD = "reset chat"
SHUTDOWN_CMD = "shutdown"
PLAY_MUSIC_CMD = "play music"
TIME_CMD = "the time"
FACETIME_CMD = "open facetime"
PASS_CMD = "open pass"
VS_CODE = "open vs code"

SITES = {
    "youtube": "https://www.youtube.com",
    "wikipedia": "https://www.wikipedia.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "github": "https://www.github.com",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
    "spotify": "https://www.spotify.com",
    "news": "https://www.cnn.com",
    "email": "https://www.gmail.com"
}

chatStr = ""


def load_commands():
    try:
        with open(COMMANDS_FILE, 'r') as f:
            return json.load(f).get('commands', {})
    except FileNotFoundError:
        return {}


def save_commands(commands):
    with open(COMMANDS_FILE, 'w') as f:
        json.dump({'commands': commands}, f, indent=4)


commands = load_commands()


def chat(queries):
    global chatStr, commands
    chatStr += f"Captain: {queries}\nJarvis: "

    if "learn" in queries:
        response_text = learn_command(queries)
    elif queries in commands:
        response_text = execute_custom_command(queries)
    else:
        response_text = generate_response(queries)

    say(response_text)
    chatStr += f"{response_text}\n"
    return response_text


def learn_command(queries):
    try:
        _, cmd, _, action = queries.split("'")
        commands[cmd.strip()] = action.strip()
        save_commands(commands)
        return f"Learned command '{cmd.strip()}' to execute '{action.strip()}'"
    except ValueError:
        return "Please use the format: learn 'command' as 'action'"


def execute_custom_command(command):
    os.system(commands[command])
    return f"Executing {command}"


def generate_response(queries):
    try:
        client = Groq(api_key=config.groq_apikey)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": queries}
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        return response_text.strip()
    except Exception as e:
        return f"Some error occurred: {e}"


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.dynamic_energy_threshold = True
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
    if os.path.isfile(app_name):
        os.startfile(app_name)
    else:
        try:
            if os_name == "Darwin":  # macOS
                open_mac_application(app_name)
            elif os_name == "Windows":
                os.system(f"start {app_name}")
            elif os_name == "Linux":
                os.system(f"xdg-open {app_name}")
        except Exception as e:
            print(f"Error opening {app_name}: {e}")


def open_mac_application(app_name):
    if app_name == "facetime":
        os.system("open /System/Applications/FaceTime.app")
    elif app_name == "pass":
        os.system("open /Applications/Passky.app")
    elif app_name == "music":
        os.system(f"open {MUSIC_PATH}")


def open_site(site_name):
    if site_name in SITES:
        say(f"Opening {site_name}, sir...")
        webbrowser.open(SITES[site_name])


def main():
    print('Welcome to Jarvis AI')
    say("Welcome to Jarvis AI")
    while True:
        query = take_command()
        if not query:
            continue

        if query == SHUTDOWN_CMD:
            say("Goodbye, sir.")
            break

        if query == CHAT_RESET_CMD:
            global chatStr
            chatStr = ""
            say("Chat history reset.")
            continue

        if query == PLAY_MUSIC_CMD:
            open_application("music")
            continue

        if query == VS_CODE:
            open_application("C:\\Users\\hp\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
            continue

        if TIME_CMD in query:
            current_time = datetime.datetime.now().strftime("%H:%M")
            say(f"Sir, the time is {current_time}")
            continue

        if query == FACETIME_CMD:
            open_application("facetime")
            continue

        if query == PASS_CMD:
            open_application("pass")
            continue

        if any(f"open {site}" in query for site in SITES):
            site_name = query.split("open ")[1].strip()
            open_site(site_name)
            continue

        chat(query)


if __name__ == '__main__':
    main()
