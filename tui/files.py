from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Label
from textual.message import Message


class ListItem(Horizontal):
	old_name: str = ""
	new_name: str = ""

	def __init__(self, old_name: str):
		super().__init__()
		self.old_name = old_name

	def compose(self) -> ComposeResult:
		self.styles.height = "auto"
		yield Label(self.old_name)
		yield Label("->")
		yield Label(self.new_name, id="new_file_name")


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
	def __init__(self):
		super().__init__()
		self.list_item_paths: dict[str, ListItem] = {}

	def compose(self) -> ComposeResult:
		yield ImageSection(id="image_section")
		yield VideoSection(id="video_section")

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "get_new_names":
			self.post_message(Message())

	async def set_files(self, images: list[str], videos: list[str]) -> None:
		img_section = self.query_one("#image_section", Vertical)
		vid_section = self.query_one("#video_section", Vertical)

		await img_section.query("VerticalScroll").remove()
		await vid_section.query("VerticalScroll").remove()
		self.list_item_paths.clear()

		img_names: list[ListItem] = []
		vid_names: list[ListItem] = []

		for img in images:
			img_item = ListItem(Path(img).name)
			self.list_item_paths[img] = img_item
			img_names.append(img_item)
		for vid in videos:
			vid_item = ListItem(Path(vid).name)
			self.list_item_paths[vid] = vid_item
			vid_names.append(vid_item)

		img_list = VerticalScroll(*img_names, id="img_list")
		vid_list = VerticalScroll(*vid_names, id="vid_list")

		img_section.mount(img_list)
		vid_section.mount(vid_list)
