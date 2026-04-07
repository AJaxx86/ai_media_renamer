from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Collapsible, Label


class TopBar(Horizontal):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		title = Label("Settings")
		title.styles.width = "100%"
		title.styles.text_align = "center"
		title.styles.text_style = "bold"
		yield title


class SettingsPage(Screen):
	working_dir: str = ""

	def __init__(self, scan_dir: str):
		super().__init__()
		self.working_dir = scan_dir
		self.log(f"working dir set: {self.working_dir}")

	def compose(self) -> ComposeResult:
		with Vertical():
			yield TopBar()
			yield Label(f"Scan directory set to '{self.working_dir}'.")
			yield Button("Back", id="back")

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "back":
			self.app.pop_screen()
