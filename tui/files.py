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


class VideoSection(Vertical):
	def compose(self) -> ComposeResult:
		vid_label = Label("Videos")
		vid_label.styles.text_style = "bold"
		yield vid_label


class Files(Vertical):
	def compose(self) -> ComposeResult:
		yield ImageSection(id="image_section")
		yield VideoSection(id="video_section")
	
	def set_files(self, images: list[str], videos: list[str]):
		image_section = self.query_one("#image_section", Vertical)
		video_section = self.query_one("#video_section", Vertical)
		
		image_section.query(ListItem).remove()
		video_section.query(ListItem).remove()
		
		for image in images:
			image_section.mount(ListItem(Path(image).name))
		for video in videos:
			video_section.mount(ListItem(Path(video).name))