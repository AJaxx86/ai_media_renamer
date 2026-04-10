from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.widgets import Button, Label, Input, TextArea


class ScanDir(Vertical):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		yield Label("Scan Directory")
		with Horizontal() as row:
			row.styles.height = "auto"
			input = Input(placeholder="e.g. C:/Users/Steve/Pictures", id="dir_input")
			input.styles.width = "1fr"
			yield input
			yield Button("Scan", id="find_files")


class Include(Vertical):
	allow_images: bool
	allow_videos: bool

	def __init__(self, images: bool, videos: bool) -> None:
		super().__init__()
		self.allow_images = images
		self.allow_videos = videos

	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		yield Label("Include")
		with Horizontal() as row:
			row.styles.height = "auto"
			yield Button("( ) Images", id="include_images")
			yield Button("(X) Videos", id="include_videos")


class ModelConfig(Vertical):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		self.styles.margin = (0, 0, 2, 0)
		yield Label("Extra Information")
		text_area = TextArea(placeholder="If you'd like, add extra context to get more specific names.", id="user_prompt")
		text_area.styles.height = "8"
		yield text_area
		yield Label("Model")
		with Horizontal() as row:
			row.styles.height = "auto"
			model_type = Button("Cloud", id="model_type")
			model_type.styles.color = "green"
			model_type.styles.margin = (0, 3, 0, 0)
			yield model_type
			yield Button("Configure", id="model_config")


class Settings(Vertical):
	class DirSet(Message):
		def __init__(self, dir: str, allow_images: bool, allow_videos: bool):
			super().__init__()
			self.dir = dir
			self.allow_images = allow_images
			self.allow_videos = allow_videos


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

		with Horizontal() as row:
			row.styles.align = ("center", "middle")
			start_button = Button("Start Analyses", id="start_analyses")
			start_button.styles.align
			yield start_button

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "find_files":
			set_dir: str = self.query_one("#dir_input", Input).value
			self.post_message(self.DirSet(set_dir, self.include_images, self.include_videos))

		elif event.button.id == "include_images":
			self.include_images = not self.include_images
			event.button.label = f"({'X' if self.include_images else ' '}) Images"

		elif event.button.id == "include_videos":
			self.include_videos = not self.include_videos
			event.button.label = f"({'X' if self.include_videos else ' '}) Videos"

		elif event.button.id == "model_type":
			self.cloud_model = not self.cloud_model
			if self.cloud_model:
				event.button.label = "Cloud"
				event.button.styles.color = "aqua"
			else:
				event.button.label = "Local"
				event.button.styles.color = "orange"
