from openai import AsyncOpenAI
from pathlib import Path
from .file_manager import image_whitelist
import subprocess
import os
import base64
import asyncio

clip_dir: str = "tmp/"


async def get_new_name(file_path: str, target_clip_length: str, extra_context: str = "") -> str:
	client = AsyncOpenAI(
		base_url="https://openrouter.ai/api/v1",
		api_key=os.getenv("OPENROUTER_KEY")
	)

	selected_model: str = "google/gemini-3-flash-preview"
	file_name: str = Path(file_path).stem
	file_type: str = Path(file_path).suffix
	is_image: bool = file_type.lstrip(".") in image_whitelist

	system_prompt: str = f"""
	Rename this {'image' if is_image else 'video'}. The current name is {file_name}.
	Respond with nothing but the new name, that means no explanation, no file extension, etc.
	Do not use a full stop at the end of the name.
	"""
	messages: list = [{
		"role": "system",
		"content": [
			{"type": "text", "text": system_prompt}
		]
	}]

	if extra_context:
		messages.append({
			"role": "user",
			"content": [
				{"type": "text", "text": extra_context}
			]
		})

	if is_image:
		encoded = await asyncio.to_thread(encode_base64, file_path)
		messages.append({
			"role": "user",
			"content": [
				{"type": "image_url", "image_url": {"url": f"data:image/{file_type};base64,{encoded}"}}
			]
		})
	else:
		clip_path = await asyncio.to_thread(extract_clip, file_path, target_clip_length)
		if not clip_path:
			return f"Unable to clip {file_name}."
		encoded = await asyncio.to_thread(encode_base64, clip_path)
		messages.append({
			"role": "user",
			"content": [
				{"type": "video_url", "video_url": {"url": f"data:video/{file_type};base64,{encoded}"}}
			]
		})

	response = await client.chat.completions.create(
		model=selected_model,
		messages=messages
	)

	return (response.choices[0].message.content or "").strip() + file_type


def encode_base64(path) -> str:
	with open(path, "rb") as f:
		return base64.b64encode(f.read()).decode("utf-8")


def extract_clip(file_path: str, duration: str, start_time: str = "0") -> str:
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
	if result.returncode == 0:
		return clip_path
	else:
		return ""
