# TODO
# [ ] new screen for AI model config, local and cloud with ECO, BALANCED, EXPENSIVE using gemini models and CUSTOM (ADD DISCLAIMER REQUIRING VISION MODELS)

from dotenv import load_dotenv
import os
import asyncio
import shutil

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, Static, Input

from tui.settings import Settings
from tui.setup import SetupPage
from tui.files import Files
from tui.model_config import ModelConfig
from utils.file_manager import scan_dir, check_ffmpeg
from utils.api_manager import get_new_name
from utils.config_manager import get_setting, set_setting

load_dotenv()

class TopBar(Horizontal):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"

		spacer = Static("")
		spacer.styles.max_width = 8
		yield spacer

		title = Label("AI Media Renamer PRO X+ 10 (Lite)")
		title.styles.width = "100%"
		title.styles.text_align = "center"
		title.styles.text_style = "bold"
		title.styles.margin = (0, 0, 1, 0)
		yield title

		back_button = Button("<-", id="back", compact=True)
		back_button.styles.dock = "right"
		back_button.styles.max_width = 8
		yield back_button


class MediaRenamer(App):
	openrouter_key, ollama_port = get_setting("openrouter_key"), get_setting("ollama_port")
	image_paths: list[str] = []
	video_paths: list[str] = []

	def compose(self) -> ComposeResult:
		with Vertical():
			yield TopBar()
			with Horizontal():
				yield Settings()
				yield Files()

	def on_mount(self) -> None:
		if not self.openrouter_key:
			self.push_screen(SetupPage())

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "back":
			self.app.push_screen(SetupPage())

	def on_settings_open_model_config(self, event: Settings.OpenModelConfig) -> None:
		self.app.push_screen(ModelConfig())

	async def on_settings_dir_set(self, event: Settings.DirSet) -> None:
		self.image_paths, self.video_paths = scan_dir(event.dir, event.allow_images, event.allow_videos)
		if len(self.image_paths) == 0 and len(self.video_paths) == 0:
			self.notify("No images or videos found in the selected directory.", timeout=3, severity="warning")
			return
		await self.query_one(Files).set_files(self.image_paths, self.video_paths)

	async def on_settings_get_new_names(self, event: Settings.GetNewNames) -> None:
		shutil.rmtree("tmp", ignore_errors=True)
		os.makedirs("tmp", exist_ok=True)
		sem = asyncio.Semaphore(2)

		async def fetch_and_update(path: str) -> None:
			item = self.query_one(Files).list_item_paths.get(path)
			if not item:
				self.notify(f"Could not find item for path: {path}", timeout=3)
				return
			new_name_label = item.query_one("#new_file_name", Input)
			new_name_label.value = "..."
			async with sem:
				new_name = await get_new_name(path, event.clip_length)
			new_name_label.value = new_name

		include_videos: bool = self.query_one(Settings).include_videos
		if not check_ffmpeg() and include_videos:
			self.app.notify("FFMPEG not found. Please make sure FFMPEG is installed to rename videos.", severity="warning")
			return

		self.app.notify("Starting analyses, this may take some time.", timeout=3)
		await asyncio.gather(*[fetch_and_update(path) for path in self.image_paths + self.video_paths])

	async def on_settings_rename_files(self, event: Settings.RenameFiles) -> None:
		pass


if __name__ == "__main__":
	MediaRenamer().run()
