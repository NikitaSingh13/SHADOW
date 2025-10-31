import os
import zipfile
import requests
from io import BytesIO

def setup_ffmpeg():
    ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
    bin_dir = os.path.join(ffmpeg_dir, "bin")

    # Skip if already installed
    if os.path.exists(bin_dir) and os.path.isfile(os.path.join(bin_dir, "ffmpeg.exe")):
        print("✅ FFmpeg already set up.")
        return

    print("⬇️ Downloading FFmpeg (Windows build from Gyan.dev)...")

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    response = requests.get(url)
    response.raise_for_status()

    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        # Extract only the 'bin' folder
        for member in zip_ref.namelist():
            if member.endswith("ffmpeg.exe") or member.endswith("ffprobe.exe") or member.endswith("ffplay.exe"):
                filename = os.path.basename(member)
                target_path = os.path.join(bin_dir, filename)
                os.makedirs(bin_dir, exist_ok=True)
                with open(target_path, "wb") as f:
                    f.write(zip_ref.read(member))

    print("✅ FFmpeg setup completed successfully!")

if __name__ == "__main__":
    setup_ffmpeg()
