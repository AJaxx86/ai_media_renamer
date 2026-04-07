from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Collapsible, Label


class SettingsPage(Screen):
    working_dir: str = ""

    def __init__(self, scan_dir: str):
        super().__init__()
        self.working_dir = scan_dir

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Label("Settings Page")
                yield Label(self.working_dir)
            with Horizontal():
                yield Button("Back", id="back")
