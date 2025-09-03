import json
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage

from Function.Authentication.login import Login

base_dir = Path(__file__).parents[2]


def relative_to_assets(path: str) -> Path:
    return base_dir /"Frame"/ "frame_01" / "asset_frame_01" / path

def load_users_json():
    try:
        with open(base_dir/"Data"/"Authentication"/"users.json", 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

class Frame01(tk.Frame):
   def __init__(self, parent, controller):
       tk.Frame.__init__(self, parent)
       self.check_data = Login(controller)
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
       self.dn_bgimage_image = PhotoImage(file=relative_to_assets("dn_bgimage.png"))
       self.dn_bgimage = self.canvas.create_image(720.0, 512.0, image=self.dn_bgimage_image)

       self.dn_logo_image = PhotoImage(file=relative_to_assets("dn_logo.png"))
       self.dn_logo = self.canvas.create_image(726.0, 223.0, image=self.dn_logo_image)

       # Thêm các thành phần khác
       self.canvas.create_text(
           587.0,
           648.0,
           anchor="nw",
           text="Bạn chưa có tài khoản?",
           fill="#000000",
           font=("Crimson Pro SemiBold", 28 * -1)
       )

       self.canvas.create_text(
           477.0,
           463.0,
           anchor="nw",
           text="Mật khẩu:",
           fill="#000000",
           font=("Crimson Pro SemiBold", 28 * -1)
       )

       self.canvas.create_text(
           477.0,
           408.0,
           anchor="nw",
           text="Tên tài khoản:",
           fill="#000000",
           font=("Crimson Pro SemiBold", 28 * -1)
       )

       self.dn_password_image = PhotoImage(file=relative_to_assets("dn_entry.png"))
       self.dn_password_bg_image = self.canvas.create_image(799.0, 478.5, image=self.dn_password_image)
       self.dn_password = Entry(
           self,
           bd=0,
           bg="#FFFFFF",
           fg="#000716",
           highlightthickness=0,
           font=("Crimson Pro SemiBold", 20 * -1),
           show="*"

       )
       self.dn_password.place(x=670.0, y=463.0, width=258.0, height=29.0)

       self.dn_username_image = PhotoImage(file=relative_to_assets("dn_entry.png"))
       self.dn_username_bg_image = self.canvas.create_image(799.0, 423.5, image=self.dn_username_image)
       self.dn_username = Entry(
           self,
           bd=0,
           bg="#FFFFFF",
           fg="#000716",
           highlightthickness=0,
           font=("Crimson Pro SemiBold", 20 * -1)
       )
       self.dn_username.place(x=670.0, y=408.0, width=258.0, height=29.0)

       self.dn_submit_image = PhotoImage(file=relative_to_assets("dn_submit.png"))
       self.dn_submit = Button(
           self,
           image=self.dn_submit_image,
           borderwidth=0,
           highlightthickness=0,
           command=lambda: self.check_data.login_data(self.dn_username, self.dn_password),
           relief="flat"
       )
       self.dn_submit.place(x=516.0, y=543.0, width=408.0, height=50.0)

       self.dn_eye_image = PhotoImage(file=relative_to_assets("dn_eye.png"))
       self.dn_eye = Button(
           self,
           image=self.dn_eye_image,
           borderwidth=0,
           highlightthickness=0,
           relief="flat",
           command=self.toggle_password_visibility
       )
       self.dn_eye.place(x=909.0, y=469.0, width=19.0, height=19.0)

       self.dn_signin_image = PhotoImage(file=relative_to_assets("dn_signin.png"))
       self.dn_signin = Button(
           self,
           image=self.dn_signin_image,
           borderwidth=0,
           highlightthickness=0,
           command=lambda: controller.show_frame("Frame02"),
           relief="flat"
       )
       self.dn_signin.place(x=575.0, y=692.0, width=289.0, height=50.0)

       self.user_data = load_users_json()

   def toggle_password_visibility(self):
       """Chuyển đổi giữa ẩn và hiện mật khẩu"""
       if self.password_hidden:
           # Hiển thị mật khẩu
           self.dn_password.config(show="")
           self.password_hidden = False
       else:
           # Ẩn mật khẩu
           self.dn_password.config(show="*")
           self.password_hidden = True

   def on_show(self):
       """This method will be called each time Frame01 is shown."""
       # Đọc lại dữ liệu người dùng từ file users.json mỗi khi Frame01 được hiển thị lại
       self.user_data = load_users_json()  # Re-load the user data from the JSON file

