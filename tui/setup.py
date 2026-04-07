from dotenv import set_key

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, Input


class TopBar(Horizontal):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		title = Label("Setup")
		title.styles.text_style = "bold"
		title.styles.width = "100%"
		title.styles.text_align = "center"
		yield title


class Inputs(Vertical):
	def compose(self) -> ComposeResult:
		with Horizontal():
			input_widget = Input(placeholder="Enter API key", id="openrouter_key", compact=True)
			input_widget.styles.width = 50
			yield Label("Openrouter (Cloud): ")
			yield input_widget
		with Horizontal():
			input_widget = Input(placeholder="Enter Port Number", id="ollama_port", compact=True)
			input_widget.styles.width = 50
			yield Label("Ollama (Local): ")
			yield input_widget


class SetupPage(Screen):
	def compose(self) -> ComposeResult:
		with Vertical():
			yield TopBar()
			yield Inputs()
			with Horizontal() as row:
				row.styles.align = ("center", "middle")
				yield Button("Save", id="save")

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "save":
			key = self.query_one("#openrouter_key", Input)
			port = self.query_one("#ollama_port", Input)
			if not key.value and not port.value:
				self.notify("Please enter a valid key or port.", severity="error")
				return

			set_key(".env", "OPENROUTER_KEY", key.value)
			set_key(".env", "OLLAMA_PORT", port.value)
			self.app.pop_screen()
