import os
from dotenv import load_dotenv

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label

from tui.settings import SettingsPage
from tui.setup import SetupPage


class TopBar(Horizontal):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		title = Label("AI Media Renamer PRO X 10+ (Lite)")
		title.styles.width = "100%"
		title.styles.text_align = "center"
		title.styles.text_style = "bold"
		yield title


class MediaRenamer(App):
	load_dotenv()
	openrouter_key, ollama_port = os.getenv("OPENROUTER_KEY"), os.getenv("OLLAMA_PORT")
	working_dir: str = ""

	def compose(self) -> ComposeResult:
		with Vertical():
			yield TopBar()
			with Horizontal():
				yield Input(placeholder="Enter scan directory")
			with Horizontal():
				yield Button("Confirm", id="confirm")

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "confirm":
			input_widget = self.query_one(Input)
			self.working_dir = input_widget.value

			if not os.path.isdir(self.working_dir):
				self.notify(f"'{self.working_dir}' isn't a valid path.", severity="error")
				return
			self.app.push_screen(SettingsPage(scan_dir=self.working_dir))
	
	def on_mount(self) -> None:
		if not self.openrouter_key and not self.ollama_port:
			self.push_screen(SetupPage())


if __name__ == "__main__":
	MediaRenamer().run()
