import json
from pathlib import Path

from Qmess.qmess_warning.tdmk_Qmess_saimkcu import Qmess_tdmk_saimkcu
from Qmess.qmess_warning.tdmk_Qmess_saiuser import Qmess_tdmk_saiuser
from Qmess.qmess_warning.tdmk_Qmess_thieuthongtin import Qmess_tdmk_thieuthongtin
from Qmess.qmess_warning.tdmk_Qmess_saiemail import Qmess_tdmk_saiemail
from Qmess.qmess_warning.tdmk_Qmess_thanhcong import Qmess_tdmk_thanhcong
from Qmess.qmess_warning.tdmk_Qmess_error import Qmess_tdmk_error

base_dir = Path(__file__).parents[2]
class ChangePasswordFunction:
    def __init__(self, app_controller):
        self.app_controller = app_controller

    def load_user_data(self, filepath):
        """Helper function to load user data from a JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            return []

    def validate_password(self, username, old_password, new_password, confirm_password, email):
        """Kiểm tra các điều kiện cho việc thay đổi mật khẩu."""
        if not (username and old_password and new_password and confirm_password and email):
            Qmess_tdmk_thieuthongtin.show_window()
            return

        logged_in_username = self.app_controller.get_user()
        if username != logged_in_username:
            Qmess_tdmk_saiuser.show_window()
            return

    def change_password(self, username, old_password, email, new_password):
        """Thực hiện thay đổi mật khẩu."""
        if not (username and old_password and email and new_password):
            Qmess_tdmk_thieuthongtin.show_window()
            return

        users = self.load_user_data(base_dir / "Data"/"Authentication"  / "users.json")

        user = next((user for user in users if user["username"] == username), None)
        if not user:
            return

        if user["email"] != email:
            Qmess_tdmk_saiemail.show_window()
            return

        if user.get("password") != old_password:
            Qmess_tdmk_saimkcu.show_window()
            return

        user["password"] = new_password
        try:
            with open(base_dir / "Data"/"Authentication" / "users.json", 'w', encoding='utf-8') as file:
                json.dump(users, file, ensure_ascii=False, indent=4)
            Qmess_tdmk_thanhcong.show_window()
        except Exception as e:
            Qmess_tdmk_error.show_window()
