import whisper
from googletrans import Translator
import ffmpeg
import os
import tkinter as tk
from tkinter import filedialog

# Load the Whisper model
model = whisper.load_model("base")  # You can use "small", "medium", or "large" for better accuracy

# Function to convert audio format
def convert_audio(input_file, output_file):
    ffmpeg.input(input_file).output(output_file).run()

# Function to transcribe audio in English
def transcribe_audio(audio_file):
    # Transcribe audio using Whisper, specifying English as the transcription language
    result = model.transcribe(audio_file, language="en")
    return result['text']

# Function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to open a file dialog and select an audio file
def upload_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select an audio file",
        filetypes=[("Audio Files", "*.wav *.mp3 *.m4a *.flac *.ogg *.aac *.wma *.mkv *.opus")]
    )
    return file_path

# Main function
def main():
    input_audio_path = upload_file()  # Get the audio file from user input
    if not input_audio_path:
        print("No file selected. Exiting...")
        return

    output_audio_path = 'output_audio.wav'

    # Convert audio file
    convert_audio(input_audio_path, output_audio_path)

    # Transcribe audio
    transcription = transcribe_audio(output_audio_path)
    print("Transcription:", transcription)

    # Translate to Hindi (assuming English is the source language)
    translation_hi = translate_text(transcription, 'hi')
    
    print("Translation (Hindi):", translation_hi)

    # Clean up
    os.remove(output_audio_path)  # Remove the temporary WAV file

if __name__ == "__main__":
    main()