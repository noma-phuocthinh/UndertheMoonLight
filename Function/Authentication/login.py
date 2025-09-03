import json
import os
import tkinter as tk
from pathlib import Path
import imageio
import threading
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer

from Qmess.qmess_warning.dn_Qmess_dntc import Qmess_dntc
from Qmess.qmess_warning.dn_Qmess_chuadktk import Qmess_chuadktk
from Qmess.qmess_warning.dn_Qmess_chuanhaptkmk import Qmess_chuanhaptkmk
from Qmess.qmess_warning.dn_Qmess_saimk import Qmess_saimatkhau

class Login:
    def __init__(self, controller, json_file=None):
        self.controller = controller
        self.video_running = False
        self.video_label = None
        self.skip_button = None

        # Xác định thư mục gốc của dự án
        self.base_path = Path(__file__).parents[2]  # Dự án nằm ở cấp 2 so với file này

        # Nếu không truyền json_file, sử dụng đường dẫn mặc định
        self.json_file = json_file or (self.base_path / "Data" / "Authentication" / "users.json")

        self.users = self.read_data()  # Đọc dữ liệu khi khởi tạo

    def read_data(self):
        """Đọc dữ liệu từ file JSON"""
        if not os.path.exists(self.json_file):
            return []
        try:
            with open(self.json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    def check_login(self, username, password):
        """Kiểm tra username và password"""
        self.users = self.read_data()  # Đọc lại dữ liệu mỗi khi gọi hàm này
        for user in self.users:
            if user["username"].lower() == username.lower():
                if user["password"] == password:
                    return user  # Đăng nhập thành công
                else:
                    Qmess_saimatkhau.show_window(self.controller.root)  # Thông báo mật khẩu sai
                    return None
        Qmess_chuadktk.show_window(self.controller.root)  # Thông báo tài khoản chưa đăng ký
        return None

    def save_history(self, username):
        """Lưu lịch sử đăng nhập"""
        history_file = self.base_path / "Data" / "Authentication" / "history.json"
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as file:
                    history_data = json.load(file)
            except json.JSONDecodeError:
                history_data = []
        else:
            history_data = []
        history_data.append({"user_name": username})

        with open(history_file, "w", encoding="utf-8") as file:
            json.dump(history_data, file, indent=2, ensure_ascii=False)

    def login_data(self, username_entry, password_entry):
        """Xử lý đăng nhập"""
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            Qmess_chuanhaptkmk.show_window(self.controller.root)  # Thông báo chưa nhập đủ thông tin
            return

        # Kiểm tra đăng nhập
        user = self.check_login(username, password)
        if user:
            self.controller.set_username(username, password)
            self.save_history(username)  # Đăng nhập thành công và phát video
            Qmess_dntc.show_window(self.controller.root, on_close=self.play_video)
        else:
            pass

    def play_video(self):
        """ Phát video sau khi đăng nhập thành công """
        self.video_running = True  # Đánh dấu đang chạy video

        # Xóa video cũ và nút Skip nếu tồn tại
        if self.video_label:
            self.video_label.destroy()
            self.video_label = None
        if self.skip_button:
            self.skip_button.destroy()
            self.skip_button = None

        # Tạo lại Label hiển thị video
        self.video_label = tk.Label(self.controller.root)
        self.video_label.place(x=0, y=0, width=1440, height=1024)

        # Load ảnh nút Skip
        skip_image_path = self.base_path / "Frame" / "frame_03" / "asset_frame_03" / "kb_skip.png"
        skip_img = Image.open(skip_image_path)

        self.skip_img_tk = ImageTk.PhotoImage(skip_img)

        # Tạo lại nút Skip với ảnh
        self.skip_button = tk.Button(
            self.controller.root, image=self.skip_img_tk, borderwidth=0, relief="flat",
            command=self.skip_video
        )
        self.skip_button.place(x=1150, y=40, width=200, height=45)

        # Đường dẫn video
        video_path = self.base_path / "Frame" / "frame_03" / "asset_frame_03" / "kb_video.mp4"

        # Chuyển đổi video_path thành chuỗi
        video_path_str = str(video_path)

        # Kiểm tra nếu file không tồn tại
        if not os.path.exists(video_path_str):
            self.controller.show_frame("Frame04")  # Chuyển thẳng đến Frame04 nếu không có video
            return

        def stream():
            """ Chạy video trong luồng riêng """
            try:
                player = MediaPlayer(video_path_str)  # Sử dụng chuỗi đường dẫn
                reader = imageio.get_reader(video_path_str)  # Sử dụng chuỗi đường dẫn

                for frame in reader:
                    if not self.video_running:
                        break  # Nếu bị dừng thì thoát vòng lặp

                    img = Image.fromarray(frame)
                    img = img.resize((1440, 1024), Image.LANCZOS)
                    img_tk = ImageTk.PhotoImage(img)

                    self.video_label.config(image=img_tk)
                    self.video_label.image = img_tk
                    self.video_label.update_idletasks()
                    self.controller.root.after(50)
                self.controller.show_frame("Frame04")

            except Exception as e:
                self.controller.show_frame("Frame04")  # Nếu lỗi, chuyển luôn đến Frame04

        # Chạy video trong luồng riêng
        threading.Thread(target=stream, daemon=True).start()

    def skip_video(self):
        """Bỏ qua video và chuyển ngay đến Frame04"""
        self.video_running = False
        if self.video_label:
            self.video_label.place_forget()  # Ẩn video
        if self.skip_button:
            self.skip_button.place_forget()  # Ẩn nút Skip
        self.controller.show_frame("Frame04")  # Chuyển sang Frame04
