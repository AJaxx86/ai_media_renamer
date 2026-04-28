from dotenv import set_key, get_key

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, Input

from utils.config_manager import get_setting, set_setting


class TopBar(Horizontal):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		title = Label("Setup")
		title.styles.text_style = "bold"
		title.styles.width = "100%"
		title.styles.text_align = "center"
		yield title


class KeyInput(Horizontal):
	def compose(self) -> ComposeResult:
		input_widget = Input(placeholder="Enter API key", id="openrouter_key", compact=True)
		input_widget.styles.width = 50

		key: str = str(get_key(".env", "OPENROUTER_KEY")) if get_key(".env", "OPENROUTER_KEY") is not None else ""
		input_widget.value = key
		yield Label("Openrouter (Cloud): ")
		yield input_widget


class PortInput(Horizontal):
	def compose(self) -> ComposeResult:
		input_widget = Input(placeholder="Enter Port Number", id="ollama_port", compact=True)
		input_widget.styles.width = 50

		port: str = str(get_key(".env", "OLLAMA_PORT")) if get_key(".env", "OLLAMA_PORT") is not None else ""
		input_widget.value = port
		yield Label("Ollama (Local): ")
		yield input_widget


class Inputs(Vertical):
	def compose(self) -> ComposeResult:
		yield KeyInput()
		yield PortInput()


class SetupPage(Screen):
	current_openrouter_key: str = get_setting("openrouter_key")
	current_ollama_port: str = str(get_setting("ollama_port"))

	def on_mount(self) -> None:
		key = self.query_one("#openrouter_key", Input)
		port = self.query_one("#ollama_port", Input)
		key.value = self.current_openrouter_key
		port.value = self.current_ollama_port

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

			set_setting("openrouter_key", key.value)
			set_setting("ollama_port", port.value)
			self.app.pop_screen()
