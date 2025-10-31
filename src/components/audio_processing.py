# python -m src.components.audio_processing
# --------------------------------------------------------
# Converts uploaded .mp4/.mp3 files into .wav format
# and stores results inside the "processed" directory.
# --------------------------------------------------------

import os
import sys
import subprocess
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from src.logger import logging
from src.exception import CustomException

# Get root directory (2 levels up from this file)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ensure_ffmpeg_available():
    """
    Ensures FFmpeg is available for MoviePy and PyDub.
    Checks system PATH and local ffmpeg/bin directory.
    """
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("FFmpeg is available in system PATH.")
    except FileNotFoundError:
        local_ffmpeg = os.path.join(ROOT_DIR, "ffmpeg", "bin", "ffmpeg.exe")
        if os.path.exists(local_ffmpeg):
            os.environ["PATH"] += os.pathsep + os.path.dirname(local_ffmpeg)
            logging.info("Using FFmpeg from local project folder.")
        else:
            raise CustomException(
                "FFmpeg not found. Please install or place it inside the 'ffmpeg/bin' folder.",
                sys
            )

class AudioExtractor:
    def __init__(self, input_dir="uploads", output_dir="processed"):
        # join with ROOT_DIR so it always points to project root folders
        self.input_dir = os.path.join(ROOT_DIR, input_dir)
        self.output_dir = os.path.join(ROOT_DIR, output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        ensure_ffmpeg_available()  # check before processing any audio/video

    def extract_audio(self, filename):
        try:
            input_path = os.path.join(self.input_dir, filename)
            output_audio_path = os.path.join(
                self.output_dir, os.path.splitext(filename)[0] + ".wav"
            )

            if not os.path.exists(input_path):
                raise CustomException(f"Input file not found: {input_path}", sys)

            logging.info(f"Processing file: {filename}")

            # Step 1: if MP4 → convert to audio
            if filename.endswith(".mp4"):
                clip = VideoFileClip(input_path)
                clip.audio.write_audiofile(output_audio_path)
                clip.close()

            # Step 2: if MP3 → convert to WAV
            elif filename.endswith(".mp3"):
                sound = AudioSegment.from_mp3(input_path)
                sound.export(output_audio_path, format="wav")

            else:
                raise CustomException("Unsupported file format", sys)

            logging.info(f"Audio extracted and saved to: {output_audio_path}")
            return output_audio_path

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    extractor = AudioExtractor()
    file_name = "sample.mp4"   # make sure uploads/sample.mp4 exists
    extractor.extract_audio(file_name)
