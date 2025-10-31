# 🧠 SHADOW – AI Meeting Summarizer Setup Guide

----------------------------------------------------------
## 1️⃣ Clone the Repository
----------------------------------------------------------
git clone https://github.com/NikitaSingh13/Shadow.git
cd Shadow

📝 Note:
System mein **Anaconda install** hona chahiye tabhi `conda` kaam karega.
Agar Anaconda nahi hai, to normal Python virtual environment bhi use kar sakte ho.
Dono ke syntax neeche diye gaye hain 👇

----------------------------------------------------------
## 2️⃣ Create & Activate Virtual Environment
----------------------------------------------------------


### 🔵 : Using Local Virtual Env (if no Anaconda)
Create env inside project folder:
conda create -p venv python==3.10 -y

Activate env:
conda activate C:\Users\<your_user>\Desktop\Shadow\venv || ya jo bhi path ho 

Deactivate env:
conda deactivate


----------------------------------------------------------
## 3️⃣ Install Dependencies
----------------------------------------------------------
Make sure virtual environment is activated before this step 👇
pip install -r requirements.txt


----------------------------------------------------------
## 4️⃣ Setup FFmpeg (Required for MoviePy & Whisper)
----------------------------------------------------------
python setup_ffmpeg.py


----------------------------------------------------------
## 5️⃣ Folder Structure Overview
----------------------------------------------------------
Shadow/
│
├── src/
│   ├── components/
│   │   ├── audio_processing.py
│   │   ├── transcription.py
│   │   └── summarization.py   # optional
│   ├── pipeline/
│   │   └── meeting_pipeline.py
│   ├── logger.py
│   └── exception.py
│
├── uploads/        # place your .mp4 or .mp3 meeting files here
├── processed/      # auto-generated .wav files
├── transcripts/    # generated text files
├── summaries/      # generated summaries (if summarization added)
│
├── requirements.txt
├── setup_ffmpeg.py
├── setup.py
├── .gitignore
├── README.md
└── venv


----------------------------------------------------------
## 6️⃣ How to Run
----------------------------------------------------------

Step 1️⃣: uploads folder mein koi bhi .mp4 file daal do (name = sample.mp4)

Step 2️⃣: Run the main pipeline command 👇
python -m src.pipeline.meeting_pipeline

➡️ This will:
- Extract audio from MP4 → processed/sample.wav
- Transcribe audio → transcripts/sample.txt
- Summarize text → summaries/sample_summary.txt (if enabled)

If these folders don’t auto-create, make them manually once:
uploads/, processed/, transcripts/, summaries/

Then re-run the same command.


----------------------------------------------------------
## 7️⃣ Logs
----------------------------------------------------------
All log files are automatically created inside the `logs/` folder.
If the pipeline crashes, check the latest log file for details.


----------------------------------------------------------
## ✅ You're Ready!
----------------------------------------------------------
Now you can:
- Upload any meeting recording (.mp4/.mp3)
- Run the pipeline
- Automatically get transcription and summaries!
