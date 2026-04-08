from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Collapsible, Label, Input, TextArea


class ScanDir(Vertical):
	def compose(self) -> ComposeResult:
		yield Label("Scan Directory")
		with Horizontal():
			yield Input("e.g. C:/Users/Steve/Pictures")
			yield Button("Scan", id="find_files")


class Include(Vertical):
	allow_images: bool
	allow_videos: bool

	def __init__(self, images: bool, videos: bool) -> None:
		super().__init__()
		self.allow_images = images
		self.allow_videos = videos

	def compose(self) -> ComposeResult:
		yield Label("Include")
		with Horizontal():
			yield Button(f"[{"X" if self.allow_images else " "}] Images", id="include_images")
			yield Button(f"[{"X" if self.allow_videos else " "}] Videos", id="include_videos")


class ModelConfig(Vertical):
	def compose(self) -> ComposeResult:
		yield Label("Extra Information")
		yield TextArea(placeholder="If you'd like, add extra context to get more specific names.", id="user_prompt")
		yield Label("Model")
		with Horizontal():
			model_type = Button("Cloud", id="model_type")
			model_type.styles.color = "green"
			yield model_type


class Settings(Vertical):
	working_dir: str = ""
	images: list[str] = []
	videos: list[str] = []

	include_images: bool = False
	include_videos: bool = True
	
	cloud_model: bool = True

	def compose(self) -> ComposeResult:
		yield ScanDir()
		yield Include(self.include_images, self.include_videos)
		yield ModelConfig()

		start_button = Button("Start Analyses", id="start_analyses")
		yield start_button

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "find_files":
			pass

		elif event.button.id == "include_images":
			self.include_images = not self.include_images
			event.button.label = f"[{'X' if self.include_images else ' '}] Images"

		elif event.button.id == "include_videos":
			self.include_videos = not self.include_videos
			event.button.label = f"[{'X' if self.include_videos else ' '}] Videos"
		
		elif event.button.id == "model_type":
			self.cloud_model = not self.cloud_model
			if self.cloud_model == True:
				event.button.label = "[Cloud]"
				event.button.styles.color = "blue"
			else:
				event.button.label = "[Local]"
				event.button.styles.color = "orange"