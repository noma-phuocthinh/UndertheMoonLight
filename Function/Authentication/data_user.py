import json
import os
from pathlib import Path
from tkinter import filedialog
import imageio
import tkinter as tk
from ffpyplayer.player import MediaPlayer
from PIL import Image, ImageTk
import threading
import re
from Qmess.qmess_warning.kb_Qmess_khongduthongtin import Qmess_khongduthongtin_kb
from Qmess.qmess_warning.kb_Qmess_nhapsaiqc import Qmess_nhapsaiqc_kb
from Qmess.qmess_warning.kb_Qmess_gender import Qmess_gender_kb
from Qmess.qmess_warning.kb_Qmess_kbtc import Qmess_kbtc
from Qmess.qmess_warning.kb_Qmess_image import Qmess_image_kb
from Qmess.qmess_warning.kb_Qmess_bio import Qmess_kb_saibio

import shutil
class Information:
    def __init__(self, controller, ui):
        self.controller = controller
        self.ui = ui  # Reference to the UI (Frame03)
        self.selected_gender = None
        self.video_running = False
        self.video_label = None
        self.avatar_path = None  # Path to the avatar image
        # Đường dẫn gốc của dự án (base directory)
        self.base_dir = Path(__file__).parents[2]  # Dự án nằm ở cấp 2 so với file này

    def choose_avatar(self):
        """Opens a file dialog to choose an avatar image"""
        file_path = filedialog.askopenfilename(
            title="Choose Avatar",
            filetypes=[("Image files", "*.png;*.jpga;*.jpeg;*.gif;*.bmp")]
        )
        if file_path:
            self.avatar_path = file_path  # Save the file path

            # Display the avatar in the UI
            username = getattr(self.controller, "current_username", None)
            if not username:
                return

            user_images_dir = self.base_dir /"Data"/ "A_User" / f"{username}_imgs"
            os.makedirs(user_images_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

            # Đường dẫn lưu avatar
            user_avatar_path = user_images_dir / f"{username}_avt.png"

            # Sao chép ảnh vào thư mục user
            shutil.copy(file_path, user_avatar_path)

            img = Image.open(file_path)
            img = img.resize((100, 100), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.ui.kb_avatar_added.config(image=img_tk)
            self.ui.kb_avatar_added.image = img_tk  # Keep a reference to the image

    def validate_dob(self, dob):
        """Kiểm tra ngày sinh có đúng định dạng DD/MM/YYYY không"""
        return bool(re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", dob)) if isinstance(dob, str) else False

    def click_gender(self, gender):
        """Xử lý chọn giới tính và cập nhật hình ảnh nút tương ứng."""

        # Kiểm tra nếu giới tính được chọn đã thay đổi
        if gender == "Nam":
            # Nếu chọn Nam, nút Nam sẽ được chọn, nút Nữ sẽ không được chọn
            self.ui.kb_sex_male.config(image=self.ui.kb_sex_male_clicked_image)  # Hình ảnh đã chọn cho Nam
            self.ui.kb_sex_female.config(image=self.ui.kb_sex_female_image)  # Hình ảnh chưa chọn cho Nữ
            self.selected_gender = "Nam"  # Cập nhật giới tính đã chọn
        elif gender == "Nữ":
            # Nếu chọn Nữ, nút Nữ sẽ được chọn, nút Nam sẽ không được chọn
            self.ui.kb_sex_female.config(image=self.ui.kb_sex_female_clicked_image)  # Hình ảnh đã chọn cho Nữ
            self.ui.kb_sex_male.config(image=self.ui.kb_sex_male_image)  # Hình ảnh chưa chọn cho Nam
            self.selected_gender = "Nữ"  # Cập nhật giới tính đã chọn

    def save_user_info(self, fullname_entry, birthday_entry, profile_entry):
        """Save the user's information to a JSON file"""
        full_name = fullname_entry.get().strip()
        dob = birthday_entry.get().strip()
        bio = profile_entry.get().strip()

        if not full_name or not dob:
            Qmess_khongduthongtin_kb.show_window()
            return

        if not self.selected_gender:
            Qmess_gender_kb.show_window()
            return

        if not self.validate_dob(dob):
            Qmess_nhapsaiqc_kb.show_window()
            return

        if not self.avatar_path:
            Qmess_image_kb.show_window()
            return

        if len(bio) > 50:
            Qmess_kb_saibio.show_window()
            return

        # Save to JSON file
        self.save_to_json(full_name, dob, bio)
        # Simulate successful save
        Qmess_kbtc.show_window(on_close=self.play_video)


    def save_to_json(self, full_name, dob, bio):
        """Lưu thông tin người dùng vào JSON với username làm key"""
        username = getattr(self.controller, "current_username", None)

        user_data = []
        file_path = self.base_dir / "Data"/"Authentication" / "users_data.json"

        # Kiểm tra xem file tồn tại không
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}  # Nếu lỗi đọc file, đặt thành dict rỗng
        else:
            data = {}

        if username in data:
            pass
        else:
            pass

        # Lưu thông tin vào key tương ứng với username
            # Cập nhật thông tin người dùng
            data[username] = {
                "full_name": full_name,
                "dob": dob,
                "bio": bio,
                "gender": self.selected_gender,
                "avatar":  str(self.base_dir /"Data"/ "A_User" / f"{username}_imgs" / f"{username}_avt.png")  # Lưu đường dẫn avatar
            }

        # Ghi dữ liệu trở lại file JSON
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def play_video(self):
        """Play a video after saving information"""
        self.video_running = True

        # Tạo một Label mới để hiển thị video
        if self.video_label is None:
            self.video_label = tk.Label(self.ui)  # Tạo Label trong Frame03
            self.video_label.place(x=0, y=0, width=1440, height=1024)  # Đặt kích thước và vị trí

        # Tải hình ảnh cho nút Skip
        skip_image_path = self.base_dir / "Frame" / "frame_03" / "asset_frame_03" / "kb_skip.png"
        skip_img = Image.open(skip_image_path)
        self.skip_img_tk = ImageTk.PhotoImage(skip_img)  # Giữ tham chiếu tránh bị xóa bởi garbage collector

        # Tạo nút Skip với hình ảnh
        self.skip_button = tk.Button(
            self.ui, image=self.skip_img_tk, borderwidth=0, relief="flat",
            command=self.skip_video)
        self.skip_button.place(x=1150, y=40, width=200, height=45)

        # Sử dụng đường dẫn tuyệt đối đến file video
        video_path = self.base_dir / "Frame" / "frame_03" / "asset_frame_03" / "kb_video.mp4"
        video_path_str = str(video_path)  # Chuyển đường dẫn từ WindowsPath sang string

        # Kiểm tra xem file video có tồn tại không
        if not os.path.exists(video_path_str):
            return

        def stream():
            """Chạy video trong luồng riêng"""
            try:
                player = MediaPlayer(video_path_str)  # Chuyển video_path thành string
                reader = imageio.get_reader(video_path_str)

                for frame in reader:
                    if not self.video_running:
                        break

                    # Chuyển đổi frame thành hình ảnh và hiển thị lên Label
                    img = Image.fromarray(frame)
                    img = img.resize((1440, 1024), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)

                    self.video_label.config(image=img_tk)
                    self.video_label.image = img_tk  # Giữ tham chiếu tránh bị thu gom rác
                    self.video_label.update_idletasks()
                    self.ui.after(50)  # Cập nhật giao diện

                # Khi video kết thúc, chuyển sang Frame04
                self.controller.show_frame("Frame01")

            except Exception :
                self.controller.show_frame("Frame01")  # Nếu lỗi, chuyển luôn đến Frame01

        # Chạy video trong một luồng riêng
        threading.Thread(target=stream, daemon=True).start()

    def skip_video(self):
        """Skip the video and go to Frame04"""
        self.video_running = False  # Dừng video
        self.video_label.place_forget()  # Ẩn video
        self.skip_button.place_forget()  # Ẩn nút Skip
        self.controller.show_frame("Frame01")  # Chuyển sang Frame01

