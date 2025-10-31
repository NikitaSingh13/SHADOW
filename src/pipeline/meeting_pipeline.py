# meeting_pipeline.py
# --------------------------------------------------------
# End-to-End Pipeline for AI Meeting Summarizer
# Converts MP4/MP3 → WAV → Transcript → Summary
# --------------------------------------------------------

import os
import sys
from src.logger import logger
from src.exception import CustomException

# Import components
from src.components.audio_processing import AudioExtractor
from src.components.transcription import Transcriber
from src.components.summarization import Summarizer  # Now included

class MeetingPipeline:
    """
    Runs the full meeting summarization workflow:
    1️⃣ Extract audio (MP4/MP3 → WAV)
    2️⃣ Transcribe (WAV → Text)
    3️⃣ Summarize (Text → Summary)
    """

    def __init__(self):
        # Initialize all components
        self.audio_extractor = AudioExtractor()
        self.transcriber = Transcriber()
        self.summarizer = Summarizer()

        # Get project root directory
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def run(self, filename):
        """
        Executes the complete meeting summarization pipeline.
        """
        try:
            logger.info(f"🚀 Starting AI Meeting Summarization pipeline for: {filename}")

            # Step 1️⃣: Audio Extraction
            audio_path = self.audio_extractor.extract_audio(filename)
            if not os.path.exists(audio_path):
                raise CustomException(f"Audio extraction failed for {filename}", sys)
            logger.info(f"✅ Audio extracted successfully: {audio_path}")

            # Step 2️⃣: Transcription
            audio_filename = os.path.basename(audio_path)
            transcript_path = self.transcriber.transcribe_audio(audio_filename)
            if not os.path.exists(transcript_path):
                raise CustomException(f"Transcription failed for {audio_filename}", sys)
            logger.info(f"✅ Transcription completed: {transcript_path}")

            # Step 3️⃣: Summarization
            transcript_filename = os.path.basename(transcript_path)
            summary_path = self.summarizer.summarize(transcript_filename)
            if not os.path.exists(summary_path):
                raise CustomException(f"Summarization failed for {transcript_filename}", sys)

            logger.info(f"🎯 Pipeline completed successfully! Summary saved at: {summary_path}")

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    pipeline = MeetingPipeline()
    file_name = "sample.mp4"  # ensure uploads/sample.mp4 exists
    pipeline.run(file_name)
