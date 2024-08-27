import sounddevice as sd
import numpy as np
import speech_recognition as sr
import requests
import json
import os
from scipy.io.wavfile import write
from gtts import gTTS
import pygame
import time

# Parameters
api_url = 'http://127.0.0.1:5000/translate'
language_current = 'en'  # Current language
language_expected = 'bn'  # Target language for translation
duration = 30  # Duration for the loop
chunk_duration = 3  # Record and translate in chunks of 5 seconds
audio_file = 'input.wav'

# Record audio from the microphone in chunks
def record_audio(filename, duration=5, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()
    write(filename, fs, recording)

# Convert audio to text using Speech Recognition
def audio_to_text(filename, language='en'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""

# Function to send translation request
def translate_text(text, current_language, expected_language):
    data = {
        'conversation': text,
        'conversationCurrentLanguage': current_language,
        'expectedOutputLanguage': expected_language
    }
    response = requests.post(api_url, json=data)
    response_data = json.loads(response.text)
    translated_text = response_data.get('translatedConversation', '')
    return translated_text

# Play the translated text
def play_text(text):
    try:
        print("Playing...")
        tts = gTTS(text, lang=language_expected)
        tts.save('output.mp3')
        
        pygame.mixer.init()
        pygame.mixer.music.load('output.mp3')
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Stop and uninitialize the mixer
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        # Remove the audio file after playback is complete
        os.remove('output.mp3')
    except Exception as e:
        print(f"Error during TTS processing: {e}")

# Main process loop
start_time = time.time()

while time.time() - start_time < duration:
    record_audio(audio_file, duration=chunk_duration)
    text = audio_to_text(audio_file, language=language_current)
    print(f"Recognized text: {text}")
    
    if text:
        translated_text = translate_text(text, language_current, language_expected)
        print(f"Translated text: {translated_text}")
        
        # Play the translated text
        play_text(translated_text)
    
    # Clean up the audio file
    os.remove(audio_file)
