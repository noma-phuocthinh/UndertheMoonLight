from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage

from Function.Settings.func import open_website
from Function.effect import create_hover_button

base_dir = Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Frame"/"frame_11"/"asset_frame_11"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Frame11(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # lambda đảm bảo khi nhấn nút thì hàm mới chạy nếu ko lúc chạy file main khởi tạo Frame thì nó sẽ chạy luôn các thuộc tính
        # self.fb1_connect = lambda: open_website("https://www.facebook.com/tncgiang.gg/")
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
        self.canvas.create_image(720.0, 512.0, image=self.image_image_1)

        self.canvas.create_rectangle(35.0, 33.0, 66.0, 64.0, fill="#000000", outline="")

        self.canvas.create_text(
            720.0,
            65.0,
            anchor="center",
            text=self.controller.format_date(),
            fill="#FFFFFF",
            font=("Crimson Pro SemiBold", 40 * -1)
        )

        self.image_PT = PhotoImage(file=relative_to_assets("image_PT.png"))
        self.canvas.create_image(720.0, 324.0, image=self.image_PT)

        self.image_ThienTruc = PhotoImage(file=relative_to_assets("image_ThienTruc.png"))
        self.canvas.create_image(450.0, 324.0, image=self.image_ThienTruc)

        self.image_CG = PhotoImage(file=relative_to_assets("image_CG.png"))
        self.canvas.create_image(180.0, 324.0, image=self.image_CG)

        self.image_TA = PhotoImage(file=relative_to_assets("image_TA.png"))
        self.canvas.create_image(990.0, 324.0, image=self.image_TA)

        self.image_ThanhTruc = PhotoImage(file=relative_to_assets("image_ThanhTruc.png"))
        self.canvas.create_image(1260.0, 324.0, image=self.image_ThanhTruc)

        # Các nút và sự kiện
        self.backhp_button_image = PhotoImage(file=relative_to_assets("backhp_button.png"))
        self.backhp_button = Button(
            self, image=self.backhp_button_image, borderwidth=0,
            highlightthickness=0, command=lambda: controller.show_frame("Frame04"),
            relief="flat"
        )
        self.backhp_button.place(x=41, y=33.0, width=36.0, height=37.0)

        self.hp_notion_image = PhotoImage(file=relative_to_assets("hp_notion.png"))
        self.hp_notion = Button(
            self, image=self.hp_notion_image, borderwidth=0,
            highlightthickness=0, command=lambda: self.controller.show_frame("Frame06"), relief="flat"
        )
        self.hp_notion.place(x=93.0, y=873.0, width=200.0, height=62.0)

        self.hp_music_image = PhotoImage(file=relative_to_assets("hp_music.png"))
        self.hp_music = Button(
            self, image=self.hp_music_image, borderwidth=0,
            highlightthickness=0, command=lambda: self.controller.show_frame("Frame07"), relief="flat"
        )
        self.hp_music.place(x=357, y=873.0, width=200.0, height=62.0)

        self.hp_tarot_image = PhotoImage(file=relative_to_assets("hp_tarot.png"))
        self.hp_tarot = Button(
            self, image=self.hp_tarot_image, borderwidth=0,
            highlightthickness=0, command=lambda: controller.show_frame("Frame09"),
            relief="flat"
        )
        self.hp_tarot.place(x=885.0, y=873.0, width=200.0, height=62.0)

        self.hp_setting_image = PhotoImage(file=relative_to_assets("hp_setting.png"))
        self.hp_setting = Button(
            self, image=self.hp_setting_image, borderwidth=0,
            highlightthickness=0, command=lambda: print("hp_setting clicked"), relief="flat"
        )
        self.hp_setting.place(x=1142.0, y=873.0, width=200.0, height=62.0)

        self.change_password_image = PhotoImage(file=relative_to_assets("change_password.png"))
        self.change_password_hover = PhotoImage(file=relative_to_assets("change_password_hover.png"))  # Ảnh hover

        self.change_password = create_hover_button(
            parent=self,
            x=252.0, y=664.0, width=421.0, height=91.0,
            img_default=self.change_password_image,
            img_hover=self.change_password_hover,
            command=lambda: self.controller.show_frame("Frame13")
        )

        self.change_infor_image = PhotoImage(file=relative_to_assets("change_infor.png"))
        self.change_infor_hover = PhotoImage(file=relative_to_assets("change_infor_hover.png"))  # Ảnh hover

        self.change_infor = create_hover_button(
            parent=self,
            x=766.0, y=664.0, width=421.0, height=91.0,
            img_default=self.change_infor_image,
            img_hover=self.change_infor_hover,
            command=lambda: self.controller.show_frame("Frame12")
        )
        #Button dang xuat
        self.hp_logout_image = PhotoImage(file=relative_to_assets("hp_logout.png"))
        self.hp_logout_hover = PhotoImage(file=relative_to_assets("hp_logout_hover.png"))
        self.hp_logout = create_hover_button(
            parent = self,
            x=1142.0, y=36.0, width=200.0, height=62.0,
            img_default=self.hp_logout_image,
            img_hover=self.hp_logout_hover,
            command=lambda: controller.show_frame("Frame01"),
        )

        #Button FB
        self.hp_facebook1_image = PhotoImage(file=relative_to_assets("hp_facebook1.png"))
        self.hp_facebook1 = Button(
            self, image=self.hp_facebook1_image, borderwidth=0,
            highlightthickness=0, command= lambda: open_website("https://www.facebook.com/tncgiang.gg"), relief="flat"
        )
        self.hp_facebook1.place(x=255, y=457.0, width=33.0, height=32.0)

        self.hp_facebook2_image = PhotoImage(file=relative_to_assets("hp_facebook2.png"))
        self.hp_facebook2 = Button(
            self, image=self.hp_facebook2_image, borderwidth=0,
            highlightthickness=0, command=lambda: open_website("https://www.facebook.com/hoang.thien.truc.101279"), relief="flat"
        )
        self.hp_facebook2.place(x=525, y=457.0, width=33.0, height=32.0)

        self.hp_facebook3_image = PhotoImage(file=relative_to_assets("hp_facebook3.png"))
        self.hp_facebook3 = Button(
            self, image=self.hp_facebook3_image, borderwidth=0,
            highlightthickness=0, command=lambda: open_website("https://www.facebook.com/thinh.bii.39/"), relief="flat"
        )
        self.hp_facebook3.place(x=795, y=457.0, width=33.0, height=32.0)

        self.hp_facebook4_image = PhotoImage(file=relative_to_assets("hp_facebook4.png"))
        self.hp_facebook4 = Button(
            self, image=self.hp_facebook4_image, borderwidth=0,
            highlightthickness=0, command=lambda: open_website("://www.facebook.com/chemend.05"), relief="flat"
        )
        self.hp_facebook4.place(x=1065, y=457.0, width=33.0, height=32.0)

        self.hp_facebook5_image = PhotoImage(file=relative_to_assets("hp_facebook5.png"))
        self.hp_facebook5 = Button(
            self, image=self.hp_facebook5_image, borderwidth=0,
            highlightthickness=0, command=lambda: open_website("https://www.facebook.com/banglinh.nguyenhoang.986"), relief="flat"
        )
        self.hp_facebook5.place(x=1335, y=457.0, width=33.0, height=32.0)





