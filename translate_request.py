import sounddevice as sd
import numpy as np
import speech_recognition as sr
import requests
import json
import os
from scipy.io.wavfile import write
from gtts import gTTS
import pygame

# Parameters
api_url = 'http://127.0.0.1:5000/translate'
language_current = 'bn'  # Bengali
language_expected = 'en'  # Target language for translation
audio_file = 'input.wav'

# Record audio from the microphone
def record_audio(filename, duration=20, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()
    print("Recording finished.")
    # Save the recording as a WAV file
    write(filename, fs, recording)

# Convert audio to text using Speech Recognition
def audio_to_text(filename, language='bn'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        # Using Google Web Speech API to recognize Bengali
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

# Function to send translation request
def translate_text(text, current_language, expected_language):
    data = {
        'conversation': text,
        'conversationCurrentLanguage': current_language,
        'expectedOutputLanguage': expected_language
    }
    response = requests.post(api_url, json=data)
    # Decode the Unicode escape sequences in the response
    response_data = json.loads(response.text)
    translated_text = response_data.get('translatedConversation', '')
    return translated_text

# Play the translated text
def play_text(text):
    try:
        tts = gTTS(text, lang=language_expected)
        tts.save('output.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('output.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        os.remove('output.mp3')
    except Exception as e:
        print(f"Error during TTS processing: {e}")

# Main process
record_audio(audio_file, duration=20)
text = audio_to_text(audio_file, language='bn')
print(f"Recognized text: {text}")

translated_text = translate_text(text, language_current, language_expected)
print(f"Translated text: {translated_text}")

# Clean up the audio file
os.remove(audio_file)

# Output translated text to file and play it
output_file = 'response_output.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(translated_text)

print(f"Translated text written to {output_file}")

play_text(translated_text)
