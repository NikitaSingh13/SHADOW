# meeting_pipeline.py
# --------------------------------------------------------
# End-to-End Pipeline for AI Meeting Summarizer
# Converts MP4/MP3 → WAV → Transcript → (Optional Summary)
# --------------------------------------------------------

import os
import sys
from src.logger import logger
from src.exception import CustomException

# Import components
from src.components.audio_processing import AudioExtractor
from src.components.transcription import Transcriber

# Optional: summarization (skip if not yet created)
try:
    from src.components.summarization import Summarizer
    SUMMARIZATION_ENABLED = True
except ImportError:
    SUMMARIZATION_ENABLED = False
    logger.warning("Summarization module not found. Skipping summary generation.")


class MeetingPipeline:
    """
    Runs the full meeting summarization workflow:
    1️⃣ Extract audio (MP4/MP3 → WAV)
    2️⃣ Transcribe (WAV → Text)
    3️⃣ Summarize (Text → Summary, optional)
    """

    def __init__(self):
        self.audio_extractor = AudioExtractor()
        self.transcriber = Transcriber()
        self.summarizer = Summarizer() if SUMMARIZATION_ENABLED else None

        # Get absolute project root (consistent with components)
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def run(self, filename):
        """
        Runs the entire pipeline for a given uploaded meeting file.
        """
        try:
            logger.info(f"Starting AI Meeting Summarization pipeline for: {filename}")

            # Step 1️⃣: Audio Extraction
            audio_path = self.audio_extractor.extract_audio(filename)
            if not os.path.exists(audio_path):
                raise CustomException(f"Audio extraction failed for {filename}", sys)

            # Step 2️⃣: Transcription
            audio_filename = os.path.basename(audio_path)
            transcript_path = self.transcriber.transcribe_audio(audio_filename)
            if not os.path.exists(transcript_path):
                raise CustomException(f"Transcription failed for {audio_filename}", sys)

            # Step 3️⃣: Summarization (optional)
            if SUMMARIZATION_ENABLED and self.summarizer:
                transcript_filename = os.path.basename(transcript_path)
                summary_path = self.summarizer.summarize(transcript_filename)
                logger.info(f"Pipeline completed successfully! Summary saved at: {summary_path}")
            else:
                logger.info(f"Pipeline completed successfully! Transcript saved at: {transcript_path}")

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    pipeline = MeetingPipeline()
    file_name = "sample.mp4"  # ensure uploads/sample.mp4 exists
    pipeline.run(file_name)
