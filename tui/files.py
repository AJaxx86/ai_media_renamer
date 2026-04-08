from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Collapsible, Label


class Images(Vertical):
	def compose(self) -> ComposeResult:
		yield Label("Images")


class Videos(Vertical):
	def compose(self) -> ComposeResult:
		yield Label("Videos")


class Files(Vertical):
	def compose(self) -> ComposeResult:
		yield Images()
		yield Videos()