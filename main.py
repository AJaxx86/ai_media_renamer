import os
from dotenv import load_dotenv
import asyncio

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, Static
from textual.message import Message

from tui.settings import Settings
from tui.setup import SetupPage
from tui.files import Files
from utils.file_manager import scan_dir
from utils.api_manager import get_new_name


class TopBar(Horizontal):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"

		spacer = Static("")
		spacer.styles.max_width = 8
		yield spacer

		title = Label("AI Media Renamer PRO X 10+ (Lite)")
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
	load_dotenv()
	openrouter_key, ollama_port = os.getenv("OPENROUTER_KEY"), os.getenv("OLLAMA_PORT")
	image_paths: list[str] = []
	video_paths: list[str] = []

	def compose(self) -> ComposeResult:
		with Vertical():
			yield TopBar()
			with Horizontal():
				yield Settings()
				yield Files()

	def on_mount(self) -> None:
		if not self.openrouter_key and not self.ollama_port:
			self.push_screen(SetupPage())

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "back":
			self.app.push_screen(SetupPage())

	async def on_settings_dir_set(self, event: Settings.DirSet) -> None:
		self.image_paths, self.video_paths = scan_dir(event.dir, event.allow_images, event.allow_videos)
		await self.query_one(Files).set_files(self.image_paths, self.video_paths)

	async def on_settings_get_new_names(self, event: Settings.GetNewNames) -> None:
		async def fetch_and_update(path: str) -> None:
			item = self.query_one(Files).list_item_paths.get(path)
			if not item:
				self.notify(f"Could not find item for path: {path}", timeout=3)
				return
			new_name_label = item.query_one("#new_file_name", Label)
			new_name_label.update("...")
			new_name = await get_new_name(path)
			new_name_label.update(new_name)

		for path in self.image_paths + self.video_paths:
			asyncio.create_task(fetch_and_update(path))

	async def on_settings_rename_files(self, event: Settings.RenameFiles) -> None:
		pass


if __name__ == "__main__":
	MediaRenamer().run()
