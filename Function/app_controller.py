import json
from datetime import datetime
import pygame
from pathlib import Path


class AppController:
    def __init__(self, root):
        self.root = root
        self.current_username = None
        self.current_user_data = None
        self.frames = {}

        # Xác định đường dẫn tương đối
        self.base_dir = Path(__file__).parents[1]  # Thư mục gốc của dự án (D:/KTLT_PJ)
        self.users_data_path = self.base_dir / "Data" / "Authentication" / "users_data.json"
        self.users_path = self.base_dir / "Data" / "Authentication" / "users.json"
        self.bg_music_path = self.base_dir / "Qmess" / "asset_component" / "bg_music.mp3"

        # Tải dữ liệu người dùng
        self.users_data = self.load_user_data(self.users_data_path)
        self.users = self.load_user_data(self.users_path)

        pygame.mixer.init()
        self.is_music_playing = False

    def load_user_data(self, filepath):
        """Helper function to load data from a JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def set_username(self, username, password):
        """Kiểm tra người dùng và mật khẩu, sau đó cập nhật dữ liệu người dùng."""
        self.users = self.load_user_data(self.users_path)
        user = next((user for user in self.users if user["username"] == username), None)
        if user and user["password"] == password:
            self.current_username = username
            self.current_user_data = self.users_data.get(username, None)  # Lấy thông tin người dùng từ dictionary
        else:
            self.current_username = None
            self.current_user_data = None

    def get_user(self):
        """Trả về tên người dùng hiện tại."""
        return self.current_username if self.current_username else "Người dùng"

    def get_name(self):
        if self.current_user_data:
            full_name = self.current_user_data.get("full_name", "Người dùng")
            words = full_name.split()  # Tách chuỗi thành danh sách các từ
            if len(words) >= 2:
                return " ".join(words[-2:])  # Lấy 2 từ cuối và nối lại
            else:
                return full_name  # Nếu tên chỉ có 1 từ, trả về nguyên tên
        else:
            return "Người dùng"

    def get_bio(self):
        """Lấy bio của người dùng hiện tại."""
        if self.current_user_data:
            return self.current_user_data.get("bio", "")  # Lấy bio từ dictionary, trả về "" nếu không có
        else:
            return ""

    def register_frame(self, frame_name, frame):
        self.frames[frame_name] = frame

    def play_music(self):
        """Chỉ phát nhạc nếu chưa phát và đang ở Frame01, Frame02, Frame03."""
        if not self.is_music_playing:
            pygame.mixer.music.load(str(self.bg_music_path))  # Chuyển đổi Path thành chuỗi
            pygame.mixer.music.play(loops=-1)  # Lặp vô hạn
            self.is_music_playing = True

    def stop_music(self):
        """Dừng nhạc nếu đang phát."""
        if self.is_music_playing:
            pygame.mixer.music.stop()
            self.is_music_playing = False

    def show_frame(self, frame_name):
        if frame_name not in ["Frame07"]:
            self.play_music()
        else:
            self.stop_music()
        if frame_name == "Frame05":
            if not self.current_username:
                return

        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()

            # Cập nhật danh sách bài hát nếu frame có hàm update_display
            if self.current_username and hasattr(frame, "update_display"):
                frame.list5 = frame.update_display()  # Gán vào thuộc tính list5 của frame

                # Nếu là Frame07 và có hàm create_music_buttons, gọi nó
                if frame_name == "Frame07" and hasattr(frame, "create_music_buttons"):
                    frame.create_music_buttons(frame.list5)
                    frame.create_music_texts()
                    frame.reset_image()

        else:
            pass

        if hasattr(frame, 'on_show'):
            frame.on_show()

    def format_date(self, date_string=None):
        if date_string is None:
            date_string = datetime.now().strftime("%Y-%m-%d")  # Chỉ lấy ngày

        try:
            date_string = date_string.split(" ")[0]  # Bỏ phần giờ nếu có
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")

            days = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"]
            months = ["", "một", "hai", "ba", "tư", "năm", "sáu", "bảy", "tám", "chín", "mười", "mười một", "mười hai"]

            weekday = days[date_obj.weekday() + 1 if date_obj.weekday() < 6 else 0]  # Fix lệch ngày
            month_name = months[date_obj.month]

            return f"{weekday}, ngày {date_obj.day} tháng {month_name}, năm {date_obj.year}"
        except ValueError:
            return 0

    def update_text_position(canvas, text_id, event):
        """Cập nhật vị trí text khi kích thước canvas thay đổi"""
        canvas.coords(text_id, event.width // 2, 65)  # Giữ chữ nằm giữa
