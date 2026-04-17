import os
import subprocess

image_whitelist: list[str] = [
	".jpg",
	".png",
]
video_whitelist: list[str] = [
	".mp4",
	".mov",
	".mkv",
]


def scan_dir(dir: str, allow_images: bool, allow_videos: bool) -> tuple[list[str], list[str]]:
	images = []
	videos = []
	for root, dirs, files in os.walk(dir):
		for file in files:
			ext = os.path.splitext(file)[1].lower()
			if ext in image_whitelist and allow_images:
				images.append(os.path.join(root, file))
			elif ext in video_whitelist and allow_videos:
				videos.append(os.path.join(root, file))
		for dir in dirs:
			scan_dir(os.path.join(root, dir), allow_images, allow_videos)
	return images, videos


def rename_files(file_paths: dict[str, str]) -> None:
	for key in file_paths:
		os.rename(key, file_paths[key])


def check_ffmpeg() -> bool:
	result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
	return result.returncode == 0
