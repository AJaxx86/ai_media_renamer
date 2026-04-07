from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, ListItem, ListView


class MediaRenamer(App):
	def compose(self) -> ComposeResult:
		with Horizontal():
			yield Label("AI Media Renamer PRO X 10+ (Lite)")
		yield ListView(
			ListItem(Label("Process Images"), id="process-images"),
			ListItem(Label("Process Videos"), id="process-videos"),
			ListItem(Label("Process Both"), id="process-both"),
			ListItem(Label("Settings"), id="settings"),
		)

	def on_list_view_selected(self, event: ListView.Selected) -> None:
		self.log(f"Selected: {event.item.id}")


if __name__ == "__main__":
	MediaRenamer().run()
