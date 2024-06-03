
# Jarvis AI Assistant

Welcome to Jarvis AI, your personal AI assistant that can perform various tasks such as opening websites, playing music, checking the time, and more. This project leverages Python's speech recognition, text-to-speech, and the OpenAI API to create an interactive assistant.

## Features

- Voice recognition to understand user commands.
- Text-to-speech for Jarvis's responses.
- Open popular websites on command.
- Open local applications like music player, FaceTime, and password manager.
- Provide the current time.
- Chat with users and generate responses using OpenAI's GPT model.

## Prerequisites

Before running the Jarvis AI, ensure you have the following installed:

- Python 3.x
- SpeechRecognition (`pip install SpeechRecognition`)
- PyAudio (`pip install PyAudio`)
- pyttsx3 (`pip install pyttsx3`)
- openai (`pip install openai`)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/jarvis-ai.git
cd jarvis-ai
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Create a `config.py` file in the project directory and add your OpenAI API key:

```python
apikey = 'your-openai-api-key'
```

## Usage

To run Jarvis AI, simply execute the main script:

```bash
python jarvis.py
```

### Voice Commands

- **Open Websites**: "open YouTube", "open Wikipedia", "open Google", etc.
- **Play Music**: "play music"
- **Check Time**: "what's the time"
- **Open Applications**: "open FaceTime", "open Pass"
- **Chat**: Any other queries will be processed by OpenAI's GPT model.

### Special Commands

- **Quit Jarvis**: "shutdown"
- **Reset Chat History**: "reset chat"

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

### Contact

If you have any questions or suggestions, feel free to open an issue or contact me directly at [itscap1810@gmail.com].

---

**Note:** Ensure you replace placeholders like `yourusername`, `your-openai-api-key`, and `your-email@example.com` with actual values.
