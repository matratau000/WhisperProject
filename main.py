# Import necessary modules
import json  # For working with JSON data format
import os  # For operating system related tasks like creating directories
import tkinter as tk  # GUI toolkit
from tkinter import filedialog  # Dialog for file selection
import whisper  # OpenAI's Whisper module for speech-to-text


# Define a function to save the transcription as a .txt file
def save_as_txt(path, transcription):
    # Open a file in write mode
    with open(path, 'w') as f:
        # Write the transcription to the file
        f.write(transcription)


# Define a function to save the transcription as a .json file
def save_as_json(path, transcription):
    # Create a dictionary to hold the transcription
    data = {
        "transcription": transcription
    }
    # Open a file in write mode
    with open(path, 'w') as f:
        # Dump the dictionary as JSON into the file
        json.dump(data, f, indent=4)


# Define the main App class for the GUI
class App:
    # Initialization method for the App class
    def __init__(self, file):
        # Reference to the main tkinter window
        self.root = file
        # Load the Whisper model for speech-to-text
        self.model = whisper.load_model("base")
        # Set the title for the main window
        self.root.title("Whisper STT GUI")

        # Create a label in the window with instructions
        self.label = tk.Label(file, text="Upload an audio file for transcription:")
        # Add some vertical padding and display the label
        self.label.pack(pady=20)

        # Create a button to upload audio files
        self.btn_upload = tk.Button(file, text="Upload", command=self.upload_audio)
        # Add some vertical padding and display the button
        self.btn_upload.pack(pady=10)

        # Create a text widget to display the transcription
        self.transcription_text = tk.Text(file, height=20, width=80)
        # Add some vertical padding and display the text widget
        self.transcription_text.pack(pady=20)

    # Define a method to transcribe audio using the Whisper model
    def transcribe(self, audio_path):
        # Use the Whisper model to transcribe the audio
        result = self.model.transcribe(audio_path)
        # Return the transcription text
        return result["text"]

    # Define a method to upload audio and get its transcription
    def upload_audio(self):
        # Display a file dialog to select an audio file
        file_path = filedialog.askopenfilename(title="Select an audio file", filetypes=(
            ("MP3 files", "*.mp3"), ("WAV files", "*.wav"), ("FLAC files", "*.flac"), ("All files", "*.*")))
        # Exit the method if no file is selected
        if not file_path:
            return
        # Get the transcription for the selected audio file
        transcription = self.transcribe(file_path)
        # Display the transcription in the text widget
        self.transcription_text.insert(tk.END, transcription)

        # Save the transcription in various formats
        # Extract the name of the audio file without its extension
        base_name = os.path.basename(file_path).rsplit('.', 1)[0]
        # Define a directory to save the transcription files
        output_directory = "transcripts"
        # Create the directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        # Save the transcription as .txt
        save_as_txt(os.path.join(output_directory, f"{base_name}.txt"), transcription)
        # Save the transcription as .json
        save_as_json(os.path.join(output_directory, f"{base_name}.json"), transcription)


# Main execution
if __name__ == "__main__":
    # Create the main tkinter window
    root = tk.Tk()
    # Instantiate the App class
    app = App(root)
    # Start the tkinter main loop
    root.mainloop()
