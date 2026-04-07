from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Input, Label

from tui.settings import SettingsPage


class MediaRenamer(App):
    working_dir: str = ""

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Label("AI Media Renamer PRO X 10+ (Lite)")
            with Horizontal():
                yield Input(placeholder="Enter scan directory")
            with Horizontal():
                yield Button("Confirm", id="confirm")

    def on_input_submitted(self, event: Input.Submitted):
        self.dir = event.value

    def on_button_pressed(self, event: Button.Pressed):
        self.app.push_screen(SettingsPage(scan_dir=self.working_dir))


if __name__ == "__main__":
    MediaRenamer().run()
