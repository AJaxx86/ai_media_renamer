from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Collapsible, Label


class ListItem(Horizontal):
	path: str = ""
	old_name: str = ""
	new_name: str = "NEW NAME"

	def __init__(self, path: str, old_name: str):
		super().__init__()
		self.path = path
		self.old_name = old_name

	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		yield Label(self.old_name)
		yield Label("->")
		yield Label(self.new_name)


class ImageSection(Vertical):
	def compose(self) -> ComposeResult:
		img_label = Label("Images")
		img_label.styles.text_style = "bold"
		yield img_label


class VideoSection(Vertical):
	def compose(self) -> ComposeResult:
		vid_label = Label("Videos")
		vid_label.styles.text_style = "bold"
		yield vid_label


class Files(Vertical):
	def compose(self) -> ComposeResult:
		yield ImageSection(id="image_section")
		yield VideoSection(id="video_section")

	def set_files(self, images: list[str], videos: list[str]) -> None:
		img_section = self.query_one("#image_section", Vertical)
		vid_section = self.query_one("#video_section", Vertical)

		img_section.query("VerticalScroll").remove()
		vid_section.query("VerticalScroll").remove()

		img_names: list[ListItem] = []
		vid_names: list[ListItem] = []

		for img in images:
			img_names.append(ListItem(img, Path(img).name))
		for vid in videos:
			vid_names.append(ListItem(vid, Path(vid).name))

		img_list = VerticalScroll(*img_names, id="img_list")
		vid_list = VerticalScroll(*vid_names, id="vid_list")

		img_section.mount(img_list)
		vid_section.mount(vid_list)
