from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
from datetime import datetime
import json
import os
import calendar
from Function.effect import create_rounded_corner_avatar

# Giữ nguyên base_dir
base_dir = Path(__file__).parents[2]


def relative_to_assets(path: str) -> Path:
    return base_dir / "Frame" / "frame_04" / "asset_frame_04" / Path(path)


class JournalEntry:
    def __init__(self, date, mood, events, sleeping_time, note, image_added):
        self.date = date
        self.mood = mood
        self.events = events
        self.sleeping_time = sleeping_time
        self.note = note
        self.image_added = image_added


class Frame04(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Biến lưu tháng và năm hiện tại
        self.current_month = datetime.today().month
        self.current_year = datetime.today().year

        # Khởi tạo danh sách các hình ảnh mood
        self.images = []
        self.day_labels = []
        # Tạo canvas
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
        self.hp_bgimage_image = PhotoImage(file=relative_to_assets("hp_bgimage.png"))
        self.hp_bgimage = self.canvas.create_image(720.0, 511.0, image=self.hp_bgimage_image)

        # Nút detail
        self.hp_detail_image = PhotoImage(file=relative_to_assets("hp_detail.png"))
        self.hp_detail = Button(
            self,
            image=self.hp_detail_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame05"),
            relief="flat"
        )
        self.hp_detail.place(x=43.0, y=47.0, width=200.0, height=62.0)

        # Nút next month
        self.hp_next_month_image = PhotoImage(file=relative_to_assets("hp_next_month.png"))
        self.hp_next_month = Button(
            self,
            image=self.hp_next_month_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.next_month,
            relief="flat"
        )
        self.hp_next_month.place(x=930.0, y=63.0, width=33.0, height=32.0)

        # Nút back month
        self.hp_back_month_image = PhotoImage(file=relative_to_assets("hp_back_month.png"))
        self.hp_back_month = Button(
            self,
            image=self.hp_back_month_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.previous_month,
            relief="flat"
        )
        self.hp_back_month.place(x=469.0, y=63.0, width=33.0, height=32.0)

        # Nút notion
        self.hp_notion_image = PhotoImage(file=relative_to_assets("hp_notion.png"))
        self.hp_notion = Button(
            self,
            image=self.hp_notion_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame06"),
            relief="flat"
        )
        self.hp_notion.place(x=93.0, y=872.0, width=200.0, height=62.0)

        # Nút music
        self.hp_music_image = PhotoImage(file=relative_to_assets("hp_music.png"))
        self.hp_music = Button(
            self,
            image=self.hp_music_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("Frame07"),
            relief="flat"
        )
        self.hp_music.place(x=357.0, y=872.0, width=200.0, height=62.0)

        # Nút tarot
        self.hp_tarot_image = PhotoImage(file=relative_to_assets("hp_tarot.png"))
        self.hp_tarot = Button(
            self,
            image=self.hp_tarot_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("Frame09"),
            relief="flat"
        )
        self.hp_tarot.place(x=885.0, y=872.0, width=200.0, height=62.0)

        # Nút setting
        self.hp_setting_image = PhotoImage(file=relative_to_assets("hp_setting.png"))
        self.hp_setting = Button(
            self,
            image=self.hp_setting_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("Frame11"),
            relief="flat"
        )
        self.hp_setting.place(x=1142.0, y=872.0, width=200.0, height=62.0)

        # Avatar
        self.hp_avatar_lb_image = PhotoImage(file=relative_to_assets("hp_avatar_lb.png"))
        self.hp_avatar_lb = self.canvas.create_image(180.0, 266.0, image=self.hp_avatar_lb_image)

        # Thông báo nhớ chúc ngủ ngon
        self.hp_health_lb_image = PhotoImage(file=relative_to_assets("hp_health_lb.png"))
        self.hp_health_lb = self.canvas.create_image(176.0, 627.0, image=self.hp_health_lb_image)

        # Tên người dùng
        self.hp_nameuser_lb_text = self.canvas.create_text(
            46.0,
            410.0,
            anchor="nw",
            text="",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 40 * -1)
        )
        # Thứ ngày
        # Thứ hai
        self.canvas.create_text(
            470.0,
            107.0,
            anchor="nw",
            text="Thứ hai",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 20 * -1)
        )

        # Thứ ba
        self.canvas.create_text(
            600.0,
            107.0,
            anchor="nw",
            text="Thứ ba",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 20 * -1)
        )

        # Thứ tư
        self.canvas.create_text(
            730.0,
            107.0,
            anchor="nw",
            text="Thứ tư",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 20 * -1)
        )

        # Thứ năm
        self.canvas.create_text(
            850.0,
            107.0,
            anchor="nw",
            text="Thứ năm",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 20 * -1)
        )

        # Thứ sáu
        self.canvas.create_text(
            980.0,
            107.0,
            anchor="nw",
            text="Thứ sáu",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 20 * -1)
        )

        # Thứ 7
        self.canvas.create_text(
            1112.0,
            107.0,
            anchor="nw",
            text="Thứ bảy",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 20 * -1)
        )

        # Chủ Nhật
        self.canvas.create_text(
            1240.0,
            107.0,
            anchor="nw",
            text="Chủ Nhật",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 20 * -1)
        )

        # Bio
        self.hp_bio_lb = self.canvas.create_text(
            46.0,
            470.0,
            anchor="nw",
            text="",
            width=350,
            fill="#FFFFFF",
            font=("Crimson Pro Italic", 20 * -1)
        )

        # Tháng và năm hiển thị
        self.hp_daynyear_lb_show = self.canvas.create_text(
            0,
            65.0,
            anchor="center",
            text="",
            justify="center",
            fill="#FFFFFF",
            font=("Crimson Pro SemiBold", 40 * -1)
        )

        # Cập nhật vị trí text khi cửa sổ thay đổi kích thước
        def update_text_position(event):
            self.canvas.coords(
                self.hp_daynyear_lb_show,
                event.width // 2,
                65.0
            )

        self.canvas.bind("<Configure>", update_text_position)

        self.image_positions = [
            (507.0, 192.0), (635.0, 192.0), (764.0, 192.0), (893.0, 192.0), (1021.0, 192.0),
            (1151.0, 192.0), (1279.0, 192.0), (506.0, 293.0), (634.0, 293.0), (763.0, 293.0),
            (892.0, 293.0), (1020.0, 293.0), (1150.0, 293.0), (1278.0, 293.0), (506.0, 394.0),
            (634.0, 394.0), (763.0, 394.0), (892.0, 394.0), (1020.0, 394.0), (1150.0, 394.0),
            (1278.0, 394.0), (506.0, 495.0), (634.0, 495.0), (763.0, 495.0), (892.0, 495.0),
            (1020.0, 495.0), (1150.0, 495.0), (1278.0, 495.0), (506.0, 596.0), (634.0, 596.0),
            (763.0, 596.0), (892.0, 596.0), (1020.0, 596.0), (1150.0, 596.0), (1278.0, 596.0),
            (507.0, 697.0), (635.0, 697.0), (764.0, 697.0), (893.0, 697.0), (1021.0, 697.0),
            (1151.0, 697.0), (1279.0, 697.0)
        ]
        self.day_positions = [(x, y + 50) for x, y in self.image_positions]
        for x, y in self.day_positions:
            label = self.canvas.create_text(
                x, y, text="", font=("Crimson Pro Bold", 11), fill="white"
            )
            self.day_labels.append(label)
        # Cập nhật giao diện ban đầu
        self.update_display()

        self.update_days_display()

    def update_display(self):
        """Cập nhật giao diện khi thay đổi tháng hoặc năm"""
        month_names = [
            "Tháng giêng", "Tháng hai", "Tháng ba", "Tháng tư", "Tháng năm", "Tháng sáu",
            "Tháng bảy", "Tháng tám", "Tháng chín", "Tháng mười", "Tháng mười một", "Tháng mười hai"
        ]
        self.canvas.itemconfig(
            self.hp_daynyear_lb_show,
            text=f"{month_names[self.current_month - 1]} {self.current_year}"
        )

        # Get the username from the controller (after login)
        username = self.controller.get_user()  # Get the username directly from the controller

        # Load user data from JSON
        try:
            # Điều chỉnh đường dẫn tương đối đến file users.json
            user_data_path = base_dir / "Data" / "Authentication" / "users_data.json"
            with open(user_data_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if username in data:
                user_data = data[username]
                self.controller.current_user_data = user_data  # Cập nhật current_user_data trong controller

                # Gọi hàm get_name và get_bio để lấy thông tin
                display_name = self.controller.get_name()  # Lấy họ và tên người dùng
                bio = self.controller.get_bio()  # Lấy bio người dùng

                # Cập nhật giao diện với họ và tên và bio
                self.canvas.itemconfig(self.hp_nameuser_lb_text, text=display_name)
                self.canvas.itemconfig(self.hp_bio_lb, text=bio)

                # Avatar handling
                user = self.controller.get_user()
                avatar_path = base_dir / "Data" / "A_User" / f"{user}_imgs" / f"{user}_avt.png"
                if os.path.exists(avatar_path):  # Kiểm tra file tồn tại
                    size = (266, 266)  # Kích thước mong muốn
                    radius = 25  # Bán kính bo góc
                    self.hp_avatar_lb_image = create_rounded_corner_avatar(avatar_path, size, radius)
                    self.canvas.itemconfig(self.hp_avatar_lb, image=self.hp_avatar_lb_image)
        except FileNotFoundError:
            return 0  # Return 0 if file not found

        # Load journal entries and update mood display
        self.load_journal_entries()
        self.update_mood_display()
        self.update_days_display()
        self.check_sleeping_time()

    def update_mood_display(self):
        """Cập nhật danh sách các ngày và mood tương ứng"""
        # Xóa các hình ảnh mood cũ
        for image in self.images:
            self.canvas.delete(image)

        # Tải danh sách các entry từ file JSON
        entries = self.load_journal_entries()

        # Tính toán các ngày trong tháng
        first_day_of_month = datetime(self.current_year, self.current_month, 1)
        week = first_day_of_month.weekday()
        days_in_month = self.dayinmonth(self.current_month, self.current_year)

        # Khởi tạo danh sách các hình ảnh mood
        self.images = []
        for i in range(40):
            if i < week or i >= week + days_in_month:
                # Ngày không thuộc tháng hiện tại
                img = PhotoImage(file=relative_to_assets("hp_mood_lb_none.png"))
            else:
                # Ngày thuộc tháng hiện tại
                day = i - week + 1
                mood = self.get_Mood(day, self.current_month, self.current_year)
                if mood:
                    img = PhotoImage(file=relative_to_assets(f"hp_mood_lb_{mood}.png"))
                else:
                    img = PhotoImage(file=relative_to_assets("hp_mood_lb_blank.png"))
            self.images.append(img)
            self.canvas.create_image(self.image_positions[i], image=img)

    def next_month(self):
        """Xử lý khi nhấn nút Next Month"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_display()

    def previous_month(self):
        """Xử lý khi nhấn nút Previous Month"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_display()

    def dayinmonth(self, month, year):
        """Trả về số ngày trong tháng"""
        if month == 2:
            return 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    def load_journal_entries(self):
        username = self.controller.get_user()
        js = base_dir / "Data" / "A_User" / f"{username}.json"
        """Tải danh sách các entry từ file JSON"""
        if js.exists():
            with open(js, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [
                    JournalEntry(entry["date"], entry["mood"], entry["event"], entry["sleeping_time"],entry["note"], entry["image_added"])
                    for entry in data
                ]
        return []

    def get_Mood(self, dd, mm, yy):
        """Lấy mood của ngày cụ thể"""
        entries = self.load_journal_entries()
        target_date = datetime(yy, mm, dd).strftime("%Y-%m-%d")
        for entry in entries:
            if not entry.date:  # Kiểm tra nếu trường date rỗng
                continue
            try:
                entry_date = datetime.strptime(entry.date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                if entry_date == target_date:
                    return entry.mood
            except ValueError:
                # Bỏ qua các entry có định dạng ngày tháng không hợp lệ
                continue
        return None

    def update_days_display(self):
        """Cập nhật các nhãn ngày trên hình tròn dựa trên tháng và năm hiện tại"""


        # Lấy số ngày trong tháng và ngày bắt đầu của tháng
        first_weekday, num_days = calendar.monthrange(self.current_year, self.current_month)

        # Xóa các nhãn ngày cũ
        for label in self.day_labels:
            self.canvas.itemconfig(label, text="")

        # Điền số ngày mới
        day = 1
        for pos in range(42):  # Có tối đa 42 ô (6 hàng x 7 cột)
            if pos >= first_weekday and day <= num_days:
                self.canvas.itemconfig(self.day_labels[pos], text=str(day))
                day += 1

    def check_sleeping_time(self):
        """Kiểm tra giấc ngủ và điều khiển hiển thị widget"""

        today_date = datetime.today().strftime("%Y-%m-%d")
        entries = self.load_journal_entries()
        # Biến kiểm tra
        found_today_entry = False
        should_show_widget = False

        for i, entry in enumerate(entries, 1):
            if not entry.date:
                continue

            try:
                # Parse và format lại ngày
                entry_date = datetime.strptime(entry.date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")

                if entry_date == today_date:
                    found_today_entry = True
                    sleeping_time = getattr(entry, 'sleeping_time', '')

                    # CHỈ hiển thị widget nếu ngủ đủ giờ
                    if sleeping_time in ["sixtoeight", "above_eight"] or sleeping_time in "":
                        should_show_widget = False
                    else:
                        should_show_widget = True
                    break

            except Exception:
                continue
        # Xử lý hiển thị widget
        if should_show_widget:
            self.hp_health_lb_image = PhotoImage(file=relative_to_assets("hp_health_lb.png"))
            self.canvas.itemconfig(self.hp_health_lb, image=self.hp_health_lb_image, state='normal')
        else:
            self.hp_health_lb_image = PhotoImage(file=relative_to_assets("hp_health_lb_un.png"))
            self.canvas.itemconfig(self.hp_health_lb, image=self.hp_health_lb_image, state='hidden')




