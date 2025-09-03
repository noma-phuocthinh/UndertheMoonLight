from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage
from Function.Authentication.data_user import Information

# Xác định đường dẫn assets
base_dir=Path(__file__).parents[2]

def relative_to_assets(path: str) -> Path:
    """Hàm để lấy đường dẫn tương đối đến thư mục assets"""
    return base_dir/"Frame"/"frame_03"/"asset_frame_03"/path

class Frame03(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Khởi tạo đối tượng Information và truyền self (Frame03) vào
        self.info_handler = Information(controller=self.controller, ui=self)

        # Canvas nền
        self.canvas = Canvas(
            self, bg="#FFFFFF", height=1024, width=1440,
            bd=0, highlightthickness=0, relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Hình nền
        self.bg_image = PhotoImage(file=relative_to_assets("kb_bgimage.png"))
        self.canvas.create_image(720.0, 512.0, image=self.bg_image)

        # Nút chọn giới tính nữ
        self.kb_sex_female_image = PhotoImage(file=relative_to_assets("kb_sex_female.png"))
        self.kb_sex_female_clicked_image = PhotoImage(file=relative_to_assets("kb_sex_female_clicked.png"))
        self.kb_sex_female = Button(
            self, image=self.kb_sex_female_image, borderwidth=0,
            highlightthickness=0, command=lambda: self.info_handler.click_gender("Nữ"), relief="flat"
        )
        self.kb_sex_female.place(x=816.0, y=460.0, width=106.0, height=45.0)

        # Nút chọn giới tính nam
        self.kb_sex_male_image = PhotoImage(file=relative_to_assets("kb_sex_male.png"))
        self.kb_sex_male_clicked_image = PhotoImage(file=relative_to_assets("kb_sex_male_clicked.png"))
        self.kb_sex_male = Button(
            self, image=self.kb_sex_male_image, borderwidth=0,
            highlightthickness=0, command=lambda: self.info_handler.click_gender("Nam"), relief="flat"
        )
        self.kb_sex_male.place(x=670.0, y=460.0, width=106.0, height=45.0)

        # Ô nhập họ tên
        self.kb_fullname = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,font=("Crimson Pro SemiBold", 20 * -1))
        self.kb_fullname.place(x=667.0, y=351.0, width=259.0, height=30.0)

        # Ô nhập ngày sinh
        self.kb_birthday = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,font=("Crimson Pro SemiBold", 20 * -1))
        self.kb_birthday.place(x=667.0, y=409.0, width=259.0, height=30.0)

        # Ô nhập tiểu sử
        self.kb_profile = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,font=("Crimson Pro SemiBold", 20 * -1))
        self.kb_profile.place(x=667.0, y=522.0, width=259.0, height=30.0)

        # Nút add avatar
        self.kb_avatar_added_image = PhotoImage(file=relative_to_assets("kb_avatar_added.png"))
        self.kb_avatar_added = Button(
            self, image=self.kb_avatar_added_image, borderwidth=0,
            highlightthickness=0, command=self.info_handler.choose_avatar, relief="flat"
        )
        self.kb_avatar_added.place(x=658.0, y=570.0, width=277.0, height=45.0)

        # Nút lưu thông tin
        self.kb_button_save_image = PhotoImage(file=relative_to_assets("kb_button_save.png"))
        self.kb_button_save = Button(
            self, image=self.kb_button_save_image, borderwidth=0,
            highlightthickness=0, command=lambda: self.info_handler.save_user_info(
                self.kb_fullname, self.kb_birthday, self.kb_profile
            ), relief="flat"
        )
        self.kb_button_save.place(x=545.0, y=669.0, width=345.0, height=50.0)

