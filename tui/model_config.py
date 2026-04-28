from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label, Input


eco_model: str = "google/gemini-3.1-flash-lite-preview"
bal_model: str = "google/gemini-3-flash-preview"
exp_model: str = "google/gemini-3.1-pro-preview"


class CloudModelConfig(Vertical):
	def compose(self) -> ComposeResult:
		self.styles.height = "auto"

		select_eco = Button("ECO", id="cloud_eco")
		select_bal = Button("BALANCED", id="cloud_bal")
		select_exp = Button("EXPENSIVE", id="cloud_exp")
		select_custom = Button("CUSTOM", id="cloud_custom")

		yield Label("Cloud Config")
		with Horizontal():
			yield select_eco
			yield select_bal
			yield select_exp
			yield select_custom
		yield Label("Custom Openrouter Model")
		yield Input(placeholder="qwen/qwen3-vl-235b-a22b-thinking")


class LocalModelConfig(Vertical):
	def compose(self) -> ComposeResult:
		yield Label("Local Config")
		yield Input(placeholder="google/gemma-4-31B-it")


class ModelConfig(Screen):
	def compose(self) -> ComposeResult:
		yield CloudModelConfig()
		yield LocalModelConfig()
