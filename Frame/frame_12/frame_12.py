import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage

from PIL import ImageTk,Image

from Function.Settings.change_inf_frame12 import UserInfoHandler

base_dir = Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Frame"/"frame_12"/"asset_frame_12"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Frame12(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.selected_gender = None

        self.username = self.controller.get_user()  # Get the username after login

        self.update_display()

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

        self.setting_bg_image = PhotoImage(file=relative_to_assets("setting_bg.png"))
        self.setting_bg = self.canvas.create_image(
            720.0,
            512.0,
            image=self.setting_bg_image
        )

        self.canvas.create_text(
            720.0,
            65.0,
            anchor="center",
            text=self.controller.format_date(),
            fill="#FFFFFF",
            font=("Crimson Pro SemiBold", 40 * -1)
        )

        self.backhp_button_image = PhotoImage(file=relative_to_assets("backhp_button.png"))
        self.backhp_button = Button(
            self,
            image=self.backhp_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame11"),
            relief="flat"
        )
        self.backhp_button.place(
            x=32.0,
            y=30.0,
            width=36.0,
            height=37.0
        )

        self.hp_music_image = PhotoImage(file=relative_to_assets("hp_music.png"))
        self.hp_music = Button(
            self,
            image=self.hp_music_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame07"),
            relief="flat"
        )
        self.hp_music.place(
            x=354.0,
            y=873.0,
            width=201.0,
            height=62.0
        )

        self.hp_notion_image = PhotoImage(file=relative_to_assets("hp_notion.png"))
        self.hp_notion = Button(
            self,
            image=self.hp_notion_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame06"),
            relief="flat"
        )
        self.hp_notion.place(
            x=91.0,
            y=873.0,
            width=200.0,
            height=62.0
        )

        self.hp_tarot_image = PhotoImage(file=relative_to_assets("hp_tarot.png"))
        self.hp_tarot = Button(
            self,
            image=self.hp_tarot_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame09"),
            relief="flat"
        )
        self.hp_tarot.place(
            x=883.0,
            y=873.0,
            width=200.0,
            height=62.0
        )

        self.hp_setting_image = PhotoImage(file=relative_to_assets("hp_setting.png"))
        self.hp_setting = Button(
            self,
            image=self.hp_setting_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame11"),
            relief="flat"
        )
        self.hp_setting.place(
            x=1140.0,
            y=873.0,
            width=200.0,
            height=62.0
        )

        # Entry fields for name, birthday, and bio
        self.setting_name_image = PhotoImage(file=relative_to_assets("setting_name.png"))
        self.setting_name_bg = self.canvas.create_image(
            822.0,
            326.5,
            image=self.setting_name_image
        )
        self.setting_name = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Crimson Pro SemiBold", 20 * -1)
        )
        self.setting_name.place(
            x=695.0,
            y=310.0,
            width=254.0,
            height=31.0
        )

        self.setting_birthday_image = PhotoImage(file=relative_to_assets("setting_birthday.png"))
        self.setting_birthday_bg = self.canvas.create_image(
            822.0,
            442.5,
            image=self.setting_birthday_image
        )
        self.setting_birthday = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Crimson Pro SemiBold", 20 * -1)
        )
        self.setting_birthday.place(
            x=695.0,
            y=426.0,
            width=254.0,
            height=31.0
        )

        self.setting_bio_image = PhotoImage(file=relative_to_assets("setting_bio.png"))
        self.setting_bio_bg = self.canvas.create_image(
            822.0,
            384.5,
            image=self.setting_bio_image
        )
        self.setting_bio = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Crimson Pro SemiBold", 20 * -1)
        )
        self.setting_bio.place(
            x=695.0,
            y=368.0,
            width=254.0,
            height=31.0
        )

        self.setting_change_ava_image = PhotoImage(file=relative_to_assets("setting_change_ava.png"))
        self.setting_change_ava = Button(
            self,
            image=self.setting_change_ava_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=self.choose_avatar
        )
        self.setting_change_ava.place(
            x=683.0,
            y=478.0,
            width=277.0,
            height=45.0
        )

        # Initialize the UserInfoHandler and pass the required parameters (controller, ui, avatar_label)
        self.user_info_handler = UserInfoHandler(controller=self.controller, ui=self, avatar_label=self.setting_change_ava)

        # Gender selection buttons
        self.setting_sex_male_image = PhotoImage(file=relative_to_assets("setting_sex_male.png"))
        self.setting_sex_male_clicked_image = PhotoImage(file=relative_to_assets("setting_sex_male_clicked.png"))
        self.setting_sex_male = Button(
            self,
            image=self.setting_sex_male_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.click_gender("Nam"),
            relief="flat"
        )
        self.setting_sex_male.place(x=694.0, y=533.0, width=106.0, height=45.0)

        self.setting_sex_female_image = PhotoImage(file=relative_to_assets("setting_sex_female.png"))
        self.setting_sex_female_clicked_image = PhotoImage(file=relative_to_assets("setting_sex_female_clicked.png"))
        self.setting_sex_female = Button(
            self,
            image=self.setting_sex_female_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.click_gender("Nữ"),
            relief="flat"
        )
        self.setting_sex_female.place(x=840.0, y=533.0, width=106.0, height=45.0)

        # Save button
        self.setting_save_image = PhotoImage(file=relative_to_assets("setting_save.png"))
        self.setting_save = Button(
            self,
            image=self.setting_save_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_user_info,
            relief="flat"
        )
        self.setting_save.place(
            x=563.0,
            y=650.0,
            width=345.0,
            height=50.0
        )
    def update_display(self):
        username = self.controller.get_user()  # Get the username directly from the controller

        # Load user data from JSON
        try:
            with open(base_dir/"Data"/"Authentication"/"users_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            if username in data:
                user_data = data[username]
                self.controller.current_user_data = user_data  # Cập nhật current_user_data trong controller

                # Lấy thông tin người dùng từ JSON
                display_name = user_data.get("full_name", "")  # Lấy họ và tên người dùng
                dob = user_data.get("dob", "")  # Lấy ngày sinh người dùng
                bio = user_data.get("bio", "")  # Lấy bio người dùng
                gender = user_data.get("gender", "")  # lấy giới tính
                # Cập nhật các Entry fields với thông tin người dùng
                self.setting_name.delete(0, tk.END)  # Xóa nội dung cũ
                self.setting_name.insert(0, display_name)  # Hiển thị tên người dùng

                self.setting_birthday.delete(0, tk.END)  # Xóa nội dung cũ
                self.setting_birthday.insert(0, dob)  # Hiển thị ngày sinh

                self.setting_bio.delete(0, tk.END)  # Xóa nội dung cũ
                self.setting_bio.insert(0, bio)  # Hiển thị bio
                if gender == "Nam":
                    self.setting_sex_male.config(image=self.setting_sex_male_clicked_image)
                    self.setting_sex_female.config(image=self.setting_sex_female_image)
                    self.selected_gender = "Nam"
                elif gender == "Nữ":
                    self.setting_sex_female.config(image=self.setting_sex_female_clicked_image)
                    self.setting_sex_male.config(image=self.setting_sex_male_image)
                    self.selected_gender = "Nữ"

                # Avatar handling
                user = self.controller.get_user()
                avatar_path = base_dir / "Data" / "A_User" / f"{user}_imgs" / f"{user}_avt.png"

                if os.path.exists(avatar_path):
                    img = Image.open(avatar_path)
                    img = img.resize((100, 100), Image.LANCZOS)  # Resize ảnh nếu cần
                    self.hp_avatar_lb_image = ImageTk.PhotoImage(img)

                    # Cập nhật hình ảnh lên button "Thêm ảnh"
                    self.setting_change_ava.config(image=self.hp_avatar_lb_image)
                    self.setting_change_ava.image = self.hp_avatar_lb_image  # Giữ tham chiếu đến ảnh để tránh bị xóa

        except FileNotFoundError:
            return 0  # Trả về 0 nếu không có file

    def choose_avatar(self):
        """Opens a file dialog to choose an avatar image"""
        self.user_info_handler.choose_avatar()

    def click_gender(self, gender):
        """Select gender and update UI"""
        self.user_info_handler.click_gender(gender)

    def save_user_info(self):
        """Save user information"""
        self.user_info_handler.save_user_info(
            self.setting_name,
            self.setting_birthday,
            self.setting_bio
        )
