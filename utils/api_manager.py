from openai import OpenAI
from pathlib import Path
import subprocess
import os
import base64

clip_dir: str = "tmp/"


async def get_new_name(file_path: str, target_clip_length: str) -> str:
	return "NEW_NAME"


def encode_base64(path) -> str:
	with open(path, "rb") as f:
		return base64.b64encode(f.read()).decode("utf-8")


def extract_clip(file_path: str, start_time: str, duration: str) -> bool:
	filename = Path(os.path.basename(file_path)).with_suffix(".mp4")
	clip_path = os.path.join(clip_dir, f"clip_{filename}")

	cmd = [
		"ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
		"-ss", str(start_time),
		"-i", str(file_path),
		"-t", str(duration),
		"-vf", "scale=-2:720",
		"-c:v", "libx264", "-preset", "ultrafast", "-crf", "30",
		"-c:a", "aac", "-b:a", "64k",
		str(clip_path)
	]
	result = subprocess.run(cmd, capture_output=True, text=True)
	return result.returncode == 0
