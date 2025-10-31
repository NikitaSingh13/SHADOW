# transcription.py
# --------------------------------------------------------
# Converts processed .wav files into text using OpenAI Whisper model.
# --------------------------------------------------------

import os
import sys
import subprocess
import whisper
from src.logger import logger
from src.exception import CustomException

# Get project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ensure_ffmpeg_available():
    """
    Ensures FFmpeg is available for Whisper (used for decoding audio).
    Checks system PATH and local ffmpeg/bin directory.
    """
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("FFmpeg is available in system PATH.")
    except FileNotFoundError:
        local_ffmpeg = os.path.join(ROOT_DIR, "ffmpeg", "bin", "ffmpeg.exe")
        if os.path.exists(local_ffmpeg):
            os.environ["PATH"] += os.pathsep + os.path.dirname(local_ffmpeg)
            logger.info("Using FFmpeg from local project folder.")
        else:
            raise CustomException(
                "FFmpeg not found. Please install or place it inside the 'ffmpeg/bin' folder.",
                sys
            )

class Transcriber:
    def __init__(self, input_dir="processed", output_dir="transcripts"):
        self.input_dir = os.path.join(ROOT_DIR, input_dir)
        self.output_dir = os.path.join(ROOT_DIR, output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        ensure_ffmpeg_available()  # ensure whisper can decode audio

        # Load Whisper model (use "base" or "small" for local CPU)
        logger.info("Loading Whisper model (base)... This may take a few seconds.")
        self.model = whisper.load_model("base")
        logger.info("Whisper model loaded successfully.")

    def transcribe_audio(self, filename):
        """
        Transcribes an audio file (.wav) into text using OpenAI Whisper.
        """
        try:
            input_path = os.path.join(self.input_dir, filename)
            output_text_path = os.path.join(self.output_dir, os.path.splitext(filename)[0] + ".txt")

            if not os.path.exists(input_path):
                raise CustomException(f"Audio file not found: {input_path}", sys)

            logger.info(f"Starting transcription for {filename}")

            # Perform transcription
            result = self.model.transcribe(input_path)
            text = result["text"]

            # Save transcript to file
            with open(output_text_path, "w", encoding="utf-8") as f:
                f.write(text.strip())

            logger.info(f"Transcription completed. Saved to: {output_text_path}")
            return output_text_path

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    transcriber = Transcriber()
    audio_filename = "sample.wav"  # make sure processed/sample.wav exists
    transcriber.transcribe_audio(audio_filename)
