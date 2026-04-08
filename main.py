import os
from dotenv import load_dotenv

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label

from tui.settings import Settings
from tui.setup import SetupPage


class TopBar(Horizontal):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		title = Label("AI Media Renamer PRO X 10+ (Lite)")
		title.styles.width = "100%"
		title.styles.text_align = "center"
		title.styles.text_style = "bold"
		yield title
		yield Button("<-", id="back")


class MediaRenamer(App):
	load_dotenv()
	openrouter_key, ollama_port = os.getenv("OPENROUTER_KEY"), os.getenv("OLLAMA_PORT")

	def compose(self) -> ComposeResult:
		with Vertical():
			yield TopBar()
			with Horizontal():
				yield Settings()

	def on_mount(self) -> None:
		if not self.openrouter_key and not self.ollama_port:
			self.push_screen(SetupPage())
	
	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "back":
			self.app.push_screen(SetupPage())


if __name__ == "__main__":
	MediaRenamer().run()
