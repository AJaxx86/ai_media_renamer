import os
from dotenv import load_dotenv

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, Static
from textual.message import Message

from tui.settings import Settings
from tui.setup import SetupPage
from tui.files import Files
from utils.get_data import scan_dir


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
		
		if event.button.id == "get_new_names":
			pass
	
	async def on_settings_dir_set(self, event: Settings.DirSet) -> None:
		images, videos = scan_dir(event.dir, event.allow_images, event.allow_videos)
		await self.query_one(Files).set_files(images, videos)


if __name__ == "__main__":
	MediaRenamer().run()
