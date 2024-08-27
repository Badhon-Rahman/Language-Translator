import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Path to the text file
file_path = 'response_output.txt'

# Read the text from the file
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
except FileNotFoundError:
    print(f"The file {file_path} does not exist.")
    exit()

# Check if the file is empty
if not text.strip():
    print(f"The file {file_path} is empty.")
    exit()

# Configure TTS engine (optional)
engine.setProperty('rate', 150)  # Set the speed of the speech
engine.setProperty('volume', 1)  # Set the volume level (0.0 to 1.0)

# Use the TTS engine to speak the text
engine.say(text)

# Wait for the speech to finish
engine.runAndWait()

print("Text has been spoken.")
