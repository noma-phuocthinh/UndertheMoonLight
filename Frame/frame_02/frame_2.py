from pathlib import Path
import tkinter as Tk
from tkinter import Canvas, Entry, Button, PhotoImage

from Function.Authentication.registeration import Registration

base_dir = Path(__file__).parents[2]


def relative_to_assets(path: str) -> Path:
    return base_dir/"Frame"/"frame_02"/"asset_frame_02"/path

class Frame02(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent)
        self.check_data = Registration(controller)
        self.controller = controller
        self.password_hidden = True
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

        # Load và hiển thị hình ảnh
        self.image_dk_bgimage = PhotoImage(file=relative_to_assets("dk_bgimage.png"))
        self.dk_bgimage = self.canvas.create_image(720.0, 512.0, image=self.image_dk_bgimage)

        # Nút đăng nhập
        self.dk_login_image = PhotoImage(file=relative_to_assets("dk_login.png"))
        self.dk_login = Button(
            self,
            image=self.dk_login_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("Frame01"),
            relief="flat"
        )
        self.dk_login.place(x=603.0, y=740.0, width=242.0, height=50.0)

        # Nút submit
        self.dk_submit_image = PhotoImage(file=relative_to_assets("dk_submit.png"))
        self.dk_submit = Button(
            self,
            image=self.dk_submit_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.check_data.register_data(self.dk_username,self.dk_password,self.dk_cfpassword,self.dk_email),
            #command=lambda: controller.show_frame("Frame03"),
            relief="flat"
        )
        self.dk_submit.place(x=578.0, y=631.0, width=292.0, height=50.0)

        # Ô nhập liệu xác nhận mật khẩu
        self.dk_cfpassword_image = PhotoImage(file=relative_to_assets("dk_entry.png"))
        self.entry_bg_1 = self.canvas.create_image(855.0, 532.5, image=self.dk_cfpassword_image)
        self.dk_cfpassword = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Crimson Pro SemiBold", 20 * -1),
            show="*"
        )
        self.dk_cfpassword.place(x=726.0, y=517.0, width=258.0, height=29.0)

        # Ô nhập liệu mật khẩu
        self.dk_password_image = PhotoImage(file=relative_to_assets("dk_entry.png"))
        self.entry_bg_2 = self.canvas.create_image(855.0, 477.5, image=self.dk_password_image)
        self.dk_password = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Crimson Pro SemiBold", 20 * -1),
            show="*"
        )
        self.dk_password.place(x=726.0, y=462.0, width=258.0, height=29.0)

        self.dk_eye_image = PhotoImage(file=relative_to_assets("dk_eye.png"))
        self.dk_eye = Button(
            self,
            image=self.dk_eye_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=self.toggle_password_visibility
        )
        self.dk_eye.place(x=965.0, y=468.0, width=19.0, height=19.0)

        # Ô nhập liệu email
        self.dk_email_image = PhotoImage(file=relative_to_assets("dk_entry.png"))
        self.entry_bg_3 = self.canvas.create_image(855.0, 419.5, image=self.dk_email_image)
        self.dk_email = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Crimson Pro SemiBold", 20 * -1)
        )
        self.dk_email.place(x=726.0, y=404.0, width=258.0, height=29.0)

        # Ô nhập liệu tên người dùng
        self.dk_username_image = PhotoImage(file=relative_to_assets("dk_entry.png"))
        self.entry_bg_4 = self.canvas.create_image(855.0, 361.5, image=self.dk_username_image)
        self.dk_username = Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Crimson Pro SemiBold", 20 * -1)
        )
        self.dk_username.place(x=726.0, y=346.0, width=258.0, height=29.0)

    def toggle_password_visibility(self):
        """Chuyển đổi giữa ẩn và hiện mật khẩu"""
        if self.password_hidden:
            # Hiển thị mật khẩu
            self.dk_password.config(show="")
            self.dk_cfpassword.config(show="")
            self.password_hidden = False
        else:
            # Ẩn mật khẩu
            self.dk_password.config(show="*")
            self.dk_cfpassword.config(show="*")
            self.password_hidden = True

