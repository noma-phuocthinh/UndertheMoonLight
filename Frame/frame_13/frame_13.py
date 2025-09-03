import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage, messagebox
from Function.Settings.change_password_frame_13 import ChangePasswordFunction  # Import lớp xử lý logic

base_dir = Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Frame"/"frame_13"/"asset_frame_13"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Frame13(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Khởi tạo lớp xử lý logic (thay đổi mật khẩu)
        self.change_password_function = ChangePasswordFunction(self.controller)

        # Khởi tạo các widget giao diện
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

        # Load background image
        try:
            self.setting_bg_password_image = PhotoImage(
                file=relative_to_assets("setting_bg_password.png"))
            self.setting_bg_password = self.canvas.create_image(
                720.0,
                512.0,
                image=self.setting_bg_password_image
            )
        except Exception :
            pass
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
            width=200.0,
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

        # Các widget nhập liệu
        self.setting_name_app = Entry(self, bd=0, bg="#FFFFFF", font=("Crimson Pro SemiBold", 20 * -1), fg="#000716", highlightthickness=0)
        self.setting_name_app.place(x=734.0, y=322.0, width=254.0, height=31.0)

        self.setting_email = Entry(self, bd=0, bg="#FFFFFF", font=("Crimson Pro SemiBold", 20 * -1), fg="#000716", highlightthickness=0)
        self.setting_email.place(x=734.0, y=380.0, width=254.0, height=31.0)

        self.setting_password_old = Entry(self, bd=0, bg="#FFFFFF", font=("Crimson Pro SemiBold", 20 * -1), fg="#000716", highlightthickness=0)
        self.setting_password_old.place(x=734.0, y=439.0, width=254.0, height=31.0)

        self.setting_password_new = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", font=("Crimson Pro SemiBold", 20 * -1), highlightthickness=0)
        self.setting_password_new.place(x=734.0, y=493.0, width=254.0, height=31.0)

        self.setting_password_again = Entry(self, bd=0, bg="#FFFFFF", font=("Crimson Pro SemiBold", 20 * -1), fg="#000716", highlightthickness=0)
        self.setting_password_again.place(x=734.0, y=554.0, width=254.0, height=31.0)

        # Nút lưu mật khẩu
        self.setting_save_password_image = PhotoImage(file=relative_to_assets("setting_save_password.png"))
        self.setting_save_password = Button(
            self,
            image=self.setting_save_password_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.change_password,  # Gọi hàm thay đổi mật khẩu
            relief="flat"
        )
        self.setting_save_password.place(x=561.169921875, y=650.0, width=346.0, height=50.0)

        # Nút quay lại
        self.backhp_button_image = PhotoImage(
            file=relative_to_assets("backhp_button.png"))
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

        self.canvas.create_text(
            720.0,
            65.0,
            anchor="center",
            text=self.controller.format_date(),
            fill="#FFFFFF",
            font=("Crimson Pro SemiBold", 40 * -1)
        )

    def change_password(self):
        """Hàm xử lý thay đổi mật khẩu khi người dùng nhấn 'Lưu mật khẩu'."""
        username = self.setting_name_app.get().strip()  # Loại bỏ khoảng trắng thừa
        old_password = self.setting_password_old.get().strip()
        email = self.setting_email.get().strip()
        new_password = self.setting_password_new.get().strip()
        confirm_password = self.setting_password_again.get().strip()

        # Kiểm tra mật khẩu và thông tin nhập vào
        validation_error = self.change_password_function.validate_password(
            username, old_password, new_password, confirm_password, email)
        if validation_error:
            return

        # Thực hiện thay đổi mật khẩu
        result = self.change_password_function.change_password(username, old_password, email, new_password)


    def show_message(self, title, message):
        """Hiển thị thông báo kết quả."""
        messagebox.showinfo(title, message)
