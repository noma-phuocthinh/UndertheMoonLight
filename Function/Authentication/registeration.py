import json
import os
import re
from pathlib import Path

# Import các thông báo lỗi
from Qmess.qmess_warning.dk_Qmess_dktc import Qmess_dktc
from Qmess.qmess_warning.dk_Qmess_gmailsai import Qmess_gmailsai
from Qmess.qmess_warning.dk_Qmess_khongduthongtin import Qmess_khongduthongtin
from Qmess.qmess_warning.dk_Qmess_mk2sai import Qmess_mk2sai
from Qmess.qmess_warning.dk_Qmess_saiquycach import Qmess_saiquycach
from Qmess.qmess_warning.dk_Qmess_tontai import Qmess_tontai


class Registration:
    def __init__(self, controller, json_file=None):
        # Đường dẫn gốc của dự án
        self.base_path = Path(__file__).parents[2]  # Lấy thư mục gốc dựa trên __file__
        self.controller = controller
        # Cập nhật đường dẫn của json_file
        self.json_file = json_file or self.base_path / "Data" / "Authentication" / "users.json"

    def read_data(self):
        """ Đọc dữ liệu từ file JSON """
        if not os.path.exists(self.json_file):
            return []
        try:
            with open(self.json_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []

    def write_data(self, data):
        """ Ghi dữ liệu vào file JSON """
        with open(self.json_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def create_user_file(self, username, email):
        """ Tạo file JSON riêng cho từng người dùng khi đăng ký trong thư mục A_User (nằm trong thư mục Data) """
        # Đặt A_User trong thư mục Data
        user_dir = self.base_path / "Data" / "A_User"
        os.makedirs(user_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

        user_file = user_dir / f"{username}.json"
        user_data = []
        with open(user_file, "w", encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)

    def create_user_images_folder(self, username):
        """ Tạo thư mục chứa hình ảnh cho người dùng với tên username_imgs """
        user_images_dir = self.base_path / "Data" / "A_User" / f"{username}_imgs"
        os.makedirs(user_images_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại

    def is_valid_gmail(self, email):
        """Kiểm tra định dạng email Gmail hợp lệ và không chứa dấu cách"""
        if " " in email:
            return False
        if "@" not in email or not email.endswith("@gmail.com"):
            return False
        email_regex = r"^[a-zA-Z0-9_.+-]+@gmail\.com$"
        if not re.match(email_regex, email):
            return False
        return True

    def is_valid_username(self, username):
        """ Kiểm tra username chỉ chứa ký tự hợp lệ """
        return username and all(char.isalnum() or char in "._" for char in username)

    def do_passwords_match(self, password, password_check):
        """ Kiểm tra mật khẩu trùng khớp """
        return password == password_check

    def register_data(self, username_entry, password_entry, password_check_entry, email_entry):
        """ Xử lý đăng ký tài khoản mới """
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        password_check = password_check_entry.get().strip()
        email = email_entry.get()

        if not all([username, password, email, password_check]):
            Qmess_khongduthongtin.show_window(self.controller.root)
            return
        users = self.read_data()

        if any(user["username"].lower() == username.lower() for user in users):
            Qmess_tontai.show_window(self.controller.root)
            return

        if any(user["email"].lower() == email.lower() for user in users):
            Qmess_tontai.show_window(self.controller.root)
            return

        if not self.is_valid_gmail(email):
            Qmess_gmailsai.show_window(self.controller.root)
            return

        if not self.is_valid_username(username):
            Qmess_saiquycach.show_window(self.controller.root)
            return

        if not self.do_passwords_match(password, password_check):
            Qmess_mk2sai.show_window(self.controller.root)
            return

        users.append({"username": username, "password": password, "email": email})
        self.write_data(users)

        # Tạo file riêng cho từng người dùng
        self.create_user_file(username, email)

        # Tạo thư mục chứa hình ảnh cho người dùng
        self.create_user_images_folder(username)

        self.controller.current_username = username  # Cập nhật username
        Qmess_dktc.show_window(self.controller.root, on_close=lambda: self.controller.show_frame("Frame03"))
