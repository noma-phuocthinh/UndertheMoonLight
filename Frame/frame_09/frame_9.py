import json
import random
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
from Qmess.qmess_warning.tr_Qmess_thongtin import Qmess_tarot
from Function.effect import create_hover_button

base_dir = Path(__file__).parents[2]
JSON_FILE = base_dir / "Data" / "Tarot" / "tarot_cards.json"
with open(JSON_FILE, "r", encoding="utf-8") as file:
    tarot_cards = json.load(file)

def relative_to_assets(path: str) -> Path:
    return base_dir / "Frame"/"frame_09"/"asset_frame_09"/Path(path)
class Frame09(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(720.0, 512.0, image=self.image_image_1)

        self.text_id = self.canvas.create_text(
            720,  # Trung tâm của 1440
            65.0,  # Y giữ nguyên
            anchor="center",  # Căn giữa theo tâm
            text=self.controller.format_date(),
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 40 * -1)
        )

        self.backhp_button_image = PhotoImage(file=relative_to_assets("backhp_button.png"))
        self.backhp_button = Button(
            self,
            image=self.backhp_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("Frame04"),
            relief="flat"
        )
        self.backhp_button.place(x=41, y=33, width=36.0, height=37.0)

        self.hp_notion_image = PhotoImage(file=relative_to_assets("hp_notion.png"))
        self.hp_notion = Button(
            self,
            image=self.hp_notion_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame06"),
            relief="flat"
        )
        self.hp_notion.place(x=93.0, y=873.0, width=200.0, height=62.0)

        self.hp_music_image = PhotoImage(file=relative_to_assets("hp_music.png"))
        self.hp_music = Button(
            self,
            image=self.hp_music_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame07"),
            relief="flat"
        )
        self.hp_music.place(x=357.0, y=873.0, width=200.0, height=62.0)

        self.hp_tarot_image = PhotoImage(file=relative_to_assets("hp_tarot.png"))
        self.hp_tarot = Button(
            self,
            image=self.hp_tarot_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("hp_tarot clicked"),
            relief="flat"
        )
        self.hp_tarot.place(x=885.0, y=873.0, width=200.0, height=62.0)

        self.hp_setting_image = PhotoImage(file=relative_to_assets("hp_setting.png"))
        self.hp_setting = Button(
            self,
            image=self.hp_setting_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("Frame11"),
            relief="flat"
        )
        self.hp_setting.place(x=1142.0, y=873.0, width=200.0, height=62.0)

        self.tarot_receive_message_image = PhotoImage(file=relative_to_assets("tarot_receive_message.png"))
        self.tarot_receive_message_hover = PhotoImage(file=relative_to_assets("tarot_receive_message_hover.png"))  # Ảnh hover
        self.tarot_receive_message = create_hover_button(
            parent=self,
            x=591.0, y=382.0, width=261.0, height=261.0,
            img_default=self.tarot_receive_message_image,
            img_hover=self.tarot_receive_message_hover,
            command=lambda: self.choose_tarot_card()
        )

        self.tarot_instruction_image = PhotoImage(file=relative_to_assets("tarot_instruction.png"))
        self.tarot_instruction_hover = PhotoImage(file=relative_to_assets("tarot_instruction_hover.png"))  # Ảnh hover

        self.tarot_instruction = create_hover_button(
            parent=self,
            x=1148.0, y=36.0, width=203.0, height=62.0,
            img_default=self.tarot_instruction_image,
            img_hover=self.tarot_instruction_hover,
            command=lambda: Qmess_tarot.show_window(self.controller.root)
        )

    def choose_tarot_card(self):
        """Chọn một lá bài Tarot ngẫu nhiên và truyền thông tin sang Frame10."""
        if not tarot_cards:
            return

        selected_card = random.choice(tarot_cards)  # Chọn lá bài ngẫu nhiên

        if "Frame10" in self.controller.frames:
            self.controller.frames["Frame10"].update_tarot_card(selected_card)  # Cập nhật Frame10
            self.controller.show_frame("Frame10")  # Chuyển đến Frame10


