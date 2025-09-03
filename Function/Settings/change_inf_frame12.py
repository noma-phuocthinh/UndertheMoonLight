import json
import os
import re
import shutil
from pathlib import Path
from tkinter import filedialog
from PIL import Image, ImageTk

from Qmess.qmess_warning.tdtt_Qmess_thieuthongtin import Qmess_tdtt_thieuthongtin
from Qmess.qmess_warning.tdtt_Qmess_saibio import Qmess_tdtt_saibio
from Qmess.qmess_warning.tdtt_Qmess_thanhcong import Qmess_tdtt_thanhcong
from Qmess.qmess_warning.tdtt_Qmess_saiquycach import Qmess_tdtt_saiquycach

base_dir = Path(__file__).parents[2]
class UserInfoHandler:
    def __init__(self, controller, ui, avatar_label):
        self.controller = controller
        self.ui = ui
        self.avatar_label = avatar_label  # Store the avatar_label to update the image in the UI
        self.selected_gender = None
        self.avatar_path = None

    def choose_avatar(self):
        """Opens a file dialog to choose an avatar image"""
        file_path = filedialog.askopenfilename(
            title="Choose Avatar",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if file_path:
            self.avatar_path = file_path  # Save the file path

            # Display the avatar in the UI
            username = getattr(self.controller, "current_username", None)
            if not username:
                return

            user_images_dir = os.path.join(base_dir / "Data"/ "A_User" / f"{username}_imgs")
            os.makedirs(user_images_dir, exist_ok=True)  # Create directory if it doesn't exist

            # Path to save avatar
            user_avatar_path = os.path.join(user_images_dir, f"{username}_avt.png")

            # Copy the image to the user folder
            shutil.copy(file_path, user_avatar_path)

            img = Image.open(file_path)
            img = img.resize((100, 100), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            # Update the image on the button (setting_change_ava)
            self.avatar_label.config(image=img_tk)
            self.avatar_label.image = img_tk  # Keep a reference to the image

    def validate_dob(self, dob):
        """Kiểm tra ngày sinh có đúng định dạng DD/MM/YYYY không"""
        return bool(re.match(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", dob)) if isinstance(dob, str) else False

    def click_gender(self, gender):
        """Xử lý chọn giới tính và cập nhật hình ảnh nút tương ứng."""
        if gender == "Nam":
            self.ui.setting_sex_male.config(image=self.ui.setting_sex_male_clicked_image)
            self.ui.setting_sex_female.config(image=self.ui.setting_sex_female_image)
            self.selected_gender = "Nam"
        elif gender == "Nữ":
            self.ui.setting_sex_female.config(image=self.ui.setting_sex_female_clicked_image)
            self.ui.setting_sex_male.config(image=self.ui.setting_sex_male_image)
            self.selected_gender = "Nữ"

    def save_user_info(self, fullname_entry, birthday_entry, profile_entry):
        """Save the user's information to a JSON file"""
        full_name = fullname_entry.get().strip()
        dob = birthday_entry.get().strip()
        bio = profile_entry.get().strip()

        if not full_name :
            Qmess_tdtt_thieuthongtin.show_window()
            return

        if not self.selected_gender:
            Qmess_tdtt_thieuthongtin.show_window()
            return
        if not self.avatar_path:
            Qmess_tdtt_thieuthongtin.show_window()
            return

        if not self.validate_dob(dob):
            Qmess_tdtt_saiquycach.show_window()
            return

        if len(bio) > 50:
            Qmess_tdtt_saibio.show_window()
            return

        self.save_to_json(full_name, dob, bio)

    def save_to_json(self, full_name, dob, bio):
        """Lưu thông tin người dùng vào JSON với username làm key"""
        username = getattr(self.controller, "current_username", None)

        file_path = base_dir / "Data" / "Authentication" / "users_data.json"
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
            user_data = data[username]

            # Cập nhật các trường thông tin nếu có sự thay đổi
            if user_data["full_name"] != full_name:
                user_data["full_name"] = full_name

            if user_data["dob"] != dob:
                user_data["dob"] = dob

            if user_data["bio"] != bio:
                user_data["bio"] = bio

            if user_data["gender"] != self.selected_gender:
                user_data["gender"] = self.selected_gender

            # Kiểm tra và cập nhật avatar nếu có sự thay đổi
            if self.avatar_path and user_data["avatar"] != str(
                    base_dir / "Data" / "A_User" / f"{username}_imgs" / f"{username}_avt.png"):
                user_data["avatar"] = str(base_dir / "Data" / "A_User" / f"{username}_imgs" / f"{username}_avt.png")

        else:
            pass

        # Ghi dữ liệu trở lại file JSON chỉ nếu có sự thay đổi
        with open(file_path, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        Qmess_tdtt_thanhcong.show_window()