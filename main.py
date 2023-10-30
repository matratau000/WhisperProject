import ssl
import urllib.request
import tkinter as tk
from tkinter import filedialog
import json
import os
from pydub import AudioSegment
import whisper

ssl._create_default_https_context = ssl._create_unverified_context


# Now you can proceed to use urllib or any other library that fetches data over HTTPS


def convert_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1)  # Ensure mono audio
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")
    return wav_path


def whisper_transcribe(audio_path):
    model = whisper.load_model("small")  # Change the model size as per your requirement
    result = model.transcribe(audio_path)
    return result["text"]


def save_transcription(transcription):
    if not os.path.exists('transcripts'):
        os.makedirs('transcripts')
    with open('transcripts/transcription.txt', 'w') as txt_file:
        txt_file.write(transcription)
    with open('transcripts/transcription.json', 'w') as json_file:
        json.dump({'transcription': transcription}, json_file)


def on_upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        wav_path = convert_audio(file_path)
        transcription = whisper_transcribe(wav_path)
        if transcription:
            transcription_display.delete('1.0', tk.END)
            transcription_display.insert(tk.END, transcription)
            save_transcription(transcription)


root = tk.Tk()
root.title("Audio Transcription App")

upload_btn = tk.Button(root, text="Upload Audio File", command=on_upload)
upload_btn.pack()

transcription_display = tk.Text(root)
transcription_display.pack()

root.mainloop()
