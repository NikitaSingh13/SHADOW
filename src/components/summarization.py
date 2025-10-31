# summarization.py
# --------------------------------------------------------
# Summarizes meeting transcripts using DistilBART model.
# Input  : transcripts/*.txt
# Output : summaries/*.txt
# --------------------------------------------------------

import os
import sys
from transformers import pipeline
from src.logger import logger
from src.exception import CustomException

# Get project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Summarizer:
    def __init__(self, input_dir="transcripts", output_dir="summaries"):
        """
        Initializes summarizer and directories.
        Loads the DistilBART model for abstractive summarization.
        """
        try:
            self.input_dir = os.path.join(ROOT_DIR, input_dir)
            self.output_dir = os.path.join(ROOT_DIR, output_dir)
            os.makedirs(self.output_dir, exist_ok=True)

            logger.info("Loading DistilBART summarization model... (first time may take longer)")
            self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
            logger.info("✅ Summarization model loaded successfully.")

        except Exception as e:
            raise CustomException(e, sys)

    def summarize(self, filename):
        """
        Summarizes a given transcript file.
        """
        try:
            input_path = os.path.join(self.input_dir, filename)
            output_summary_path = os.path.join(
                self.output_dir, os.path.splitext(filename)[0] + "_summary.txt"
            )

            if not os.path.exists(input_path):
                raise CustomException(f"Transcript file not found: {input_path}", sys)

            logger.info(f"📘 Reading transcript from: {input_path}")

            with open(input_path, "r", encoding="utf-8") as f:
                transcript_text = f.read()

            if len(transcript_text.strip()) == 0:
                raise CustomException("Transcript file is empty!", sys)

            logger.info("🧠 Generating summary...")

            # Split long transcripts into smaller chunks (DistilBART limit ~1024 tokens)
            max_chunk_size = 3000
            chunks = [transcript_text[i:i + max_chunk_size] for i in range(0, len(transcript_text), max_chunk_size)]

            summary_text = ""
            for chunk in chunks:
                summary = self.summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                summary_text += summary[0]['summary_text'].strip() + "\n\n"

            with open(output_summary_path, "w", encoding="utf-8") as f:
                f.write(summary_text.strip())

            logger.info(f"✅ Summary saved to: {output_summary_path}")
            return output_summary_path

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    summarizer = Summarizer()
    transcript_file = "sample.txt"  # make sure transcripts/sample.txt exists
    summarizer.summarize(transcript_file)
