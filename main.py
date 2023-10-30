import ssl
import urllib.request
import tkinter as tk
from tkinter import filedialog
import json
import os
from pydub import AudioSegment
import whisper

# Bypass SSL verification for HTTPS requests (use with caution)
ssl._create_default_https_context = ssl._create_unverified_context


def convert_audio(file_path):
    """Convert audio to mono WAV format."""
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")
    return wav_path


def whisper_transcribe(audio_path):
    """Transcribe audio using the whisper model."""
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    return result["text"]


def save_transcription(transcription):
    """Save transcription as TXT and JSON."""
    if not os.path.exists('transcripts'):
        os.makedirs('transcripts')
    with open('transcripts/transcription.txt', 'w') as txt_file:
        txt_file.write(transcription)
    with open('transcripts/transcription.json', 'w') as json_file:
        json.dump({'transcription': transcription}, json_file)


def on_upload():
    """Upload audio, transcribe, display and save transcription."""
    file_path = filedialog.askopenfilename()
    if file_path:
        wav_path = convert_audio(file_path)
        transcription = whisper_transcribe(wav_path)
        if transcription:
            transcription_display.delete('1.0', tk.END)
            transcription_display.insert(tk.END, transcription)
            save_transcription(transcription)


# Initialize tkinter window
root = tk.Tk()
root.title("Audio Transcription App")

# Add "Upload Audio File" button
upload_btn = tk.Button(root, text="Upload Audio File", command=on_upload)
upload_btn.pack()

# Add display area for transcription
transcription_display = tk.Text(root)
transcription_display.pack()

# Start tkinter loop
root.mainloop()
