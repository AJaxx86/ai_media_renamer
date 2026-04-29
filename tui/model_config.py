from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, Input

from utils.config_manager import get_setting, set_setting

cloud_model_buttons: dict[str, Button] = {}

def change_button_colour(model: str) -> None:
	for button in cloud_model_buttons.values():
		button.styles.color = "white"
	cloud_model_buttons[model].styles.color = "green"

def initialise_cloud_model_buttons() -> None:
	model: str = get_setting("cloud_model")
	match model:
		case Models.ECO:
			change_button_colour("eco")
		case Models.BALANCED:
			change_button_colour("bal")
		case Models.EXPENSIVE:
			change_button_colour("exp")
		case _:
			change_button_colour("custom")


class Models:
	ECO: str = "google/gemini-3.1-flash-lite-preview"
	BALANCED: str = "google/gemini-3-flash-preview"
	EXPENSIVE: str = "google/gemini-3.1-pro-preview"


class CloudModelConfig(Vertical):
	def compose(self) -> ComposeResult:
		self.styles.padding = (1, 1, 2, 1)

		select_eco = Button("ECO", id="cloud_eco")
		select_bal = Button("BALANCED", id="cloud_bal")
		select_exp = Button("EXPENSIVE", id="cloud_exp")
		select_custom = Button("CUSTOM", id="cloud_custom")
		cloud_model_input = Input(placeholder="qwen/qwen3-vl-235b-a22b-thinking", id="custom_model")
		cloud_model_input.styles.width = 80

		cloud_model_buttons["eco"] = select_eco
		cloud_model_buttons["bal"] = select_bal
		cloud_model_buttons["exp"] = select_exp
		cloud_model_buttons["custom"] = select_custom
		initialise_cloud_model_buttons()

		yield Label("Cloud Config")
		with Horizontal() as h:
			h.styles.height = "auto"
			yield select_eco
			yield select_bal
			yield select_exp
			yield select_custom
		yield Label("Custom Openrouter Model")
		yield cloud_model_input


class LocalModelConfig(Vertical):
	def compose(self) -> ComposeResult:
		local_model_input = Input(placeholder="google/gemma-4-31B-it", id="local_model")
		local_model_input.styles.width = 80

		yield Label("Local Config")
		with Horizontal():
			yield local_model_input
			yield Button("Set Model", id="set_local_model")


class ModelConfig(Screen):
	def compose(self) -> ComposeResult:
		with Vertical():
			yield CloudModelConfig()
			yield LocalModelConfig()
			yield Label("NOTE: Please make sure that custom models have video support.")
			yield Button("Back", id="close_config")

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "cloud_eco":
			set_setting("cloud_model", Models.ECO)
			change_button_colour("eco")
			self.notify(f"Cloud model set to {Models.ECO}")
		elif event.button.id == "cloud_bal":
			set_setting("cloud_model", Models.BALANCED)
			change_button_colour("bal")
			self.notify(f"Cloud model set to {Models.BALANCED}")
		elif event.button.id == "cloud_exp":
			set_setting("cloud_model", Models.EXPENSIVE)
			change_button_colour("exp")
			self.notify(f"Cloud model set to {Models.EXPENSIVE}")
		elif event.button.id == "cloud_custom":
			custom_model_input = self.query_one("#custom_model", Input)
			set_setting("cloud_model", custom_model_input.value)
			change_button_colour("custom")
			self.notify(f"Cloud model set to {custom_model_input.value}")
		elif event.button.id == "set_local_model":
			local_model_input = self.query_one("#local_model", Input)
			set_setting("local_model", local_model_input.value)
			self.notify(f"Local model set to {local_model_input.value}")
		elif event.button.id == "close_config":
			self.app.pop_screen()
