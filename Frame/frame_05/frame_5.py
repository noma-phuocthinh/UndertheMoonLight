import os
from pathlib import Path
import json
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Canvas, Button, Frame, PhotoImage, ttk
import datetime
from Function.effect import round_corners

# Đường dẫn thư mục dữ liệu
base_dir = Path(__file__).parents[2]
USER_DATA_PATH = base_dir / "Data"/"A_User"
ASSETS_PATH = base_dir / "Frame"/"frame_05" / "asset_frame_05"



class CustomFrame:
    def __init__(self, parent, data, username):
        self.parent = parent
        self.data = data
        self.assets_path = ASSETS_PATH

        # Đường dẫn dữ liệu theo username
        self.user_json_file = USER_DATA_PATH / f"{username}.json"
        self.user_img_path = USER_DATA_PATH / f"{username}_imgs"

        # Frame chứa canvas
        self.frame = Frame(parent, bg="#FFFFFF")
        self.frame.pack(fill="both", expand=True, pady=10)
        self.canvas = Canvas(self.frame, bg="#FFFFFF", height=735, width=1338, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.images = {}
        self._load_images()

        # Định dạng lại ngày
        formatted_date = self._format_date(self.data["date"])
        self.canvas.create_text(297.0, 100.0, anchor="nw", text=formatted_date, width=887, fill="#000000",
                                font=("Crimson Pro SemiBold", 30))
        self.canvas.create_text(297.0, 273.0, anchor="nw", text=self.data["note"], width=887, fill="#000000",
                                font=("Crimson Pro Regular", 15))

        self._create_buttons()

    def _relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def _format_date(self, date_str):
        """Chuyển đổi ngày từ dữ liệu JSON thành dạng 'Thứ, ngày tháng năm' (hỗ trợ tiếng Việt)"""

        # Danh sách tên thứ và tháng bằng tiếng Việt
        days_vn = {
            "Monday": "Thứ hai",
            "Tuesday": "Thứ ba",
            "Wednesday": "Thứ tư",
            "Thursday": "Thứ năm",
            "Friday": "Thứ sáu",
            "Saturday": "Thứ bảy",
            "Sunday": "Chủ nhật"
        }

        months_vn = {
            "January": "giêng",
            "February": "hai",
            "March": "ba",
            "April": "tư",
            "May": "năm",
            "June": "sáu",
            "July": "bảy",
            "August": "tám",
            "September": "chín",
            "October": "mười",
            "November": "mười một",
            "December": "mười hai"
        }

        # Chuyển chuỗi ngày thành đối tượng datetime
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        # Lấy tên thứ và tháng từ datetime
        day_name = date_obj.strftime("%A")  # Lấy tên thứ (Monday, Tuesday,...)
        month_name = date_obj.strftime("%B")  # Lấy tên tháng (January, February,...)

        # Thay thế tên tiếng Anh bằng tiếng Việt
        day_vn = days_vn.get(day_name, day_name)
        month_vn = months_vn.get(month_name, month_name)

        # Format lại ngày tháng
        return f"{day_vn}, ngày {date_obj.day} tháng {month_vn} năm {date_obj.year}"

    def _load_images(self):
        self.images["bg"] = PhotoImage(file=self._relative_to_assets("detail_bg.png"))
        self.images["mood"] = PhotoImage(file=self._relative_to_assets(f"detail_{self.data['mood']}.png"))

        # Load ảnh sự kiện
        self.images["events"] = [PhotoImage(file=self._relative_to_assets(f"detail_{event}.png")) for event in
                                 self.data["event"]]
        self.images["events"] += [PhotoImage(file=self._relative_to_assets("detail_none_icon.png"))] * (
                32 - len(self.images["events"]))

        # Xử lý ảnh người dùng thêm vào
        self.images["added"] = []
        image_added_list = self.data["image_added"]

        # Nếu có ít hơn 3 ảnh, bổ sung ảnh mặc định vào danh sách
        while len(image_added_list) < 3:
            image_added_list.append("image_added.png")

        for img in image_added_list:
            img_path = self.user_img_path  / img if img != "image_added.png" else self._relative_to_assets("image_added.png")
            pil_img = Image.open(img_path)
            pil_img = pil_img.resize((232, 232), Image.Resampling.LANCZOS)
            pil_img = round_corners(pil_img, radius=30)
            pil_img = pil_img.convert("RGBA")
            tk_img = ImageTk.PhotoImage(pil_img)
            self.images["added"].append(tk_img)

        # Hiển thị ảnh nền và mood
        self.canvas.create_image(669.0, 367.0, image=self.images["bg"])
        self.canvas.create_image(124.0, 164.0, image=self.images["mood"])

        # Hiển thị ảnh sự kiện
        event_positions = [
            (316.0, 184.0), (316.0, 231.0), (368.0, 184.0), (368.0, 231.0),
            (419.0, 184.0), (419.0, 231.0), (471.0, 184.0), (471.0, 231.0),
            (521.0, 184.0), (521.0, 231.0), (573.0, 184.0), (573.0, 231.0),
            (625.0, 184.0), (625.0, 231.0), (676.0, 184.0), (676.0, 231.0),
            (728.0, 184.0), (728.0, 231.0), (780.0, 184.0), (780.0, 231.0),
            (832.0, 184.0), (832.0, 231.0), (883.0, 184.0), (883.0, 231.0),
            (935.0, 184.0), (935.0, 231.0), (985.0, 184.0), (985.0, 231.0),
            (1037.0, 184.0), (1037.0, 231.0), (1089.0, 184.0), (1089.0, 231.0)
        ]

        for img, (x, y) in zip(self.images["events"], event_positions):
            self.canvas.create_image(x, y, image=img)

        # Hiển thị ảnh người dùng thêm vào
        added_positions = [(413.0, 554.0), (740.0, 554.0), (1068.0, 554.0)]
        for img, (x, y) in zip(self.images["added"], added_positions):
            self.canvas.create_image(x, y, image=img)

    def _create_buttons(self):
        self.images["delete_btn"] = PhotoImage(file=self._relative_to_assets("detail_delete.png"))
        btn_delete = Button(self.frame, image=self.images["delete_btn"], borderwidth=0, highlightthickness=0,
                            command=self.delete_data, relief="flat")
        btn_delete.place(x=1259.0, y=19.0, width=42.0, height=39.0)

    def delete_data(self):
        try:
            # Đọc dữ liệu từ file JSON của user
            with open(self.user_json_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Tìm phần tử cần xóa dựa trên date
            target_date = self.data.get("date")
            new_data = [item for item in data if item.get("date") != target_date]

            # Nếu có phần tử bị xóa
            if len(new_data) < len(data):
                with open(self.user_json_file, "w", encoding="utf-8") as file:
                    json.dump(new_data, file, indent=4, ensure_ascii=False)

                # Xóa ảnh liên quan (trừ ảnh mặc định)
                for img_name in self.data.get("image_added", []):
                    if img_name != "image_added.png":  # Không xóa ảnh mặc định
                        img_path = self.user_img_path / img_name
                        if img_path.exists():
                            try:
                                img_path.unlink()
                            except Exception as e:
                                continue

            else:
                pass

            # Xóa frame trên giao diện
            self.frame.destroy()

        except FileNotFoundError:
           pass
        except json.JSONDecodeError:
            pass
        except Exception:
            pass


# Load dữ liệu từ JSON và tạo frame
def load_frames(parent, username):
    json_file = os.path.join(USER_DATA_PATH, f"{username}.json")  # Tạo đường dẫn động

    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)  # Đọc dữ liệu từ file JSON

        for entry in data:
            CustomFrame(parent, entry, username)

    except json.JSONDecodeError:
        pass
    except FileNotFoundError:
        pass
    except Exception:
        pass



class Frame05(tk.Frame):
   def __init__(self, parent, controller):
       tk.Frame.__init__(self, parent)
       self.controller = controller

       # Tạo main frame với nền đen
       self.main_frame = Frame(self, bg="#000000")
       self.main_frame.pack(fill="both", expand=True)

       # Tạo canvas với nền đen
       self.canvas = Canvas(
           self.main_frame,
           bg="#000000",
           height=1024,
           width=1440,
           highlightthickness=0
       )

       # Tạo scrollbar và đặt bên phải main frame
       self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
       self.scrollbar.pack(side="right", fill="y")

       # Cấu hình canvas và đặt bên trái scrollbar
       self.canvas.pack(side="left", fill="both", expand=True)
       self.canvas.configure(yscrollcommand=self.scrollbar.set)

       # Tạo inner frame
       self.inner_frame = Frame(self.canvas, bg="#000000")
       self.canvas.create_window((50, 70), window=self.inner_frame, anchor="nw")

       # Load dữ liệu vào Frame
       load_frames(self.inner_frame, self.controller.get_user())

       # Cập nhật scrollregion khi inner_frame thay đổi kích thước
       def update_scrollregion(event):
           self.canvas.configure(scrollregion=self.canvas.bbox("all"))

       self.inner_frame.bind("<Configure>", update_scrollregion)

       # Thêm các thành phần giao diện khác
       self.backhp_bg_image = PhotoImage(file=ASSETS_PATH / "backhp_bg.png")
       self.backhp_bg = self.canvas.create_image(720.0, 512.0, image=self.backhp_bg_image)

       self.backhp_button_image = PhotoImage(file=ASSETS_PATH / "backhp_button.png")
       self.backhp_button = Button(
           self,
           image=self.backhp_button_image,
           borderwidth=0,
           highlightthickness=0,
           command=lambda: self.controller.show_frame("Frame04"),
           relief="flat"
       )
       self.backhp_button.place(x=38.0, y=30.0, width=36.0, height=37.0)

   def update_display(self):
       self.username = self.controller.get_user()
       if self.username == "Người dùng":
           return

       # Xóa frame cũ trước khi load lại
       for widget in self.inner_frame.winfo_children():
           widget.destroy()

       load_frames(self.inner_frame, self.username)

