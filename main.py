import ssl
import urllib.request
import tkinter as tk
from tkinter import filedialog
import json
import os
from pydub import AudioSegment
import whisper

# Bypass SSL verification for HTTPS requests (use with caution)
# Note: This is potentially unsafe. Ensure you understand the implications of bypassing SSL verification.
ssl._create_default_https_context = ssl._create_unverified_context


def convert_audio(file_path):
    """
    Convert the given audio file to a mono WAV format.

    Parameters:
        file_path (str): Path to the audio file.

    Returns:
        str: Path to the converted WAV file.
    """
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1)  # Set to mono
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")
    return wav_path


def whisper_transcribe(audio_path):
    """
    Transcribe the given audio using the Whisper model.

    Parameters:
        audio_path (str): Path to the audio file.

    Returns:
        str: Transcribed text.
    """
    model = whisper.load_model("small")
    result = model.transcribe(audio_path)
    return result["text"]


def save_transcription(transcription):
    """
    Save the transcription in both TXT and JSON formats.

    Parameters:
        transcription (str): The transcribed text.
    """
    # Create 'transcripts' directory if it doesn't exist
    if not os.path.exists('transcripts'):
        os.makedirs('transcripts')

    # Save transcription as TXT
    with open('transcripts/transcription.txt', 'w') as txt_file:
        txt_file.write(transcription)

    # Save transcription as JSON
    with open('transcripts/transcription.json', 'w') as json_file:
        json.dump({'transcription': transcription}, json_file)


def on_upload():
    """
    Handle audio upload, transcribe the audio, display the transcription,
    and save the transcription.
    """
    # Ask user to select an audio file
    file_path = filedialog.askopenfilename()
    if file_path:
        # Convert the audio to WAV format
        wav_path = convert_audio(file_path)

        # Transcribe the audio
        transcription = whisper_transcribe(wav_path)
        if transcription:
            # Update the transcription display
            transcription_display.delete('1.0', tk.END)
            transcription_display.insert(tk.END, transcription)

            # Save the transcription
            save_transcription(transcription)


# Initialize the main tkinter window
root = tk.Tk()
root.title("Audio Transcription App")

# Create and add a button to upload audio files
upload_btn = tk.Button(root, text="Upload Audio File", command=on_upload)
upload_btn.pack()

# Create and add a text area to display transcriptions
transcription_display = tk.Text(root)
transcription_display.pack()

# Start the tkinter main loop
root.mainloop()
