from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Collapsible, Label


class ListItem(Horizontal):
	def __init__(self, old_name: str):
		super().__init__()
		self.old_name = old_name

	def compose(self) -> ComposeResult:
		yield Label(self.old_name)
		yield Label("==")
		yield Label("NEW NAME")


class ImageSection(Vertical):
	def compose(self) -> ComposeResult:
		img_label = Label("Images")
		img_label.styles.text_style = "bold"
		yield img_label

		img_list = VerticalScroll(id="img_list")
		yield img_list


class VideoSection(Vertical):
	def compose(self) -> ComposeResult:
		vid_label = Label("Videos")
		vid_label.styles.text_style = "bold"
		yield vid_label

		vid_list = VerticalScroll(id="vid_list")
		yield vid_list


class Files(Vertical):
	def compose(self) -> ComposeResult:
		yield ImageSection(id="image_section")
		yield VideoSection(id="video_section")

	def set_files(self, images: list[str], videos: list[str]):
		img_list = self.query_one("#img_list", VerticalScroll)
		vid_list = self.query_one("#vid_list", VerticalScroll)

		img_list.query(ListItem).remove()
		vid_list.query(ListItem).remove()

		for image in images:
			img_list.mount(ListItem(Path(image).name))
		for video in videos:
			vid_list.mount(ListItem(Path(video).name))
