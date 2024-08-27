from gtts import gTTS
import pygame
from langdetect import detect
import os

# Initialize pygame mixer
pygame.mixer.init()

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

# Detect the language of the text
try:
    lang = detect(text)
except Exception as e:
    print(f"Error detecting language: {e}")
    lang = 'en'  # Default to English if detection fails

# Create a gTTS object with the detected language
try:
    tts = gTTS(text, lang=lang)
    # Save the audio file
    audio_file = 'output.mp3'
    tts.save(audio_file)

    # Play the audio file
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up the audio file
    os.remove(audio_file)

    print("Text has been spoken.")
except Exception as e:
    print(f"Error during TTS processing: {e}")
