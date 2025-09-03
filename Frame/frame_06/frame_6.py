from pathlib import Path
from PIL import Image, ImageTk
import os
from tkinter import filedialog
import tkinter as tk
from tkinter import Canvas, Button, Frame, ttk
from tkinter import PhotoImage
from datetime import datetime
import json

from Qmess.qmess_warning.m_Qmess_checkdulieu import Qmess_checkdulieu
from Qmess.qmess_warning.m_Qmess_trackmooddi import Qmess_trackmooddi
from Function.effect import create_toggle_button, limit_text_input
base_dir=Path(__file__).parents[2]

class JournalFrame:
   def __init__(self, parent, controller):
       self.controller = controller
       self.parent = parent
       self.m_mood = []
       self.m_event = []
       self.m_sleeping_time = []
       self.m_image_added = []


       # Khởi tạo ASSETS_PATH
       self.ASSETS_PATH = base_dir /"Frame"/ "frame_06" / "asset_frame_06"


       # Lưu trạng thái của các button
       self.button_states = {}


       self.canvas = Canvas(
           self.parent,
           bg="#FFFFFF",
           height=2945,
           width=1271,
           bd=0,
           highlightthickness=0,
           relief="ridge"
       )
       self.canvas.pack(fill="both", expand=True)


       self.load_images()
       self.create_widgets()


   def relative_to_assets(self, path: str) -> Path:
       """Hàm lấy đường dẫn file trong thư mục asset"""
       return self.ASSETS_PATH / Path(path)


   def load_images(self):
       """Hàm load ảnh"""
       self.m_jounalframeimage_image = PhotoImage(file=self.relative_to_assets("m_jounalframeimage.png"))
       self.m_angry_image = PhotoImage(file=self.relative_to_assets("m_angry.png"))
       self.m_depressed_image = PhotoImage(file=self.relative_to_assets("m_depressed.png"))
       self.m_sad_image = PhotoImage(file=self.relative_to_assets("m_sad.png"))
       self.m_normal_image = PhotoImage(file=self.relative_to_assets("m_normal.png"))
       self.m_happy_image = PhotoImage(file=self.relative_to_assets("m_happy.png"))
       self.m_friend_image = PhotoImage(file=self.relative_to_assets("m_friend.png"))
       self.m_family_image = PhotoImage(file=self.relative_to_assets("m_family.png"))
       self.m_crush_image = PhotoImage(file=self.relative_to_assets("m_crush.png"))
       self.m_ny_image = PhotoImage(file=self.relative_to_assets("m_ny.png"))
       self.m_coworker_image = PhotoImage(file=self.relative_to_assets("m_coworker.png"))
       self.m_diff_people_image = PhotoImage(file=self.relative_to_assets("m_diff_people.png"))
       self.m_sunny_image = PhotoImage(file=self.relative_to_assets("m_sunny.png"))
       self.m_rainny_image = PhotoImage(file=self.relative_to_assets("m_rainny.png"))
       self.m_cloud_image = PhotoImage(file=self.relative_to_assets("m_cloud.png"))
       self.m_cool_image = PhotoImage(file=self.relative_to_assets("m_cool.png"))
       self.m_hot_image = PhotoImage(file=self.relative_to_assets("m_hot.png"))
       self.m_diff_weather_image = PhotoImage(file=self.relative_to_assets("m_diff_weather.png"))
       self.m_home_image = PhotoImage(file=self.relative_to_assets("m_home.png"))
       self.m_study_image = PhotoImage(file=self.relative_to_assets("m_study.png"))
       self.m_work_image = PhotoImage(file=self.relative_to_assets("m_work.png"))
       self.m_eating_image = PhotoImage(file=self.relative_to_assets("m_eating.png"))
       self.m_shopping_image = PhotoImage(file=self.relative_to_assets("m_shopping.png"))
       self.m_travel_image = PhotoImage(file=self.relative_to_assets("m_travel.png"))
       self.m_hospital_image = PhotoImage(file=self.relative_to_assets("m_hospital.png"))
       self.m_clean_image = PhotoImage(file=self.relative_to_assets("m_clean.png"))
       self.m_movie_image = PhotoImage(file=self.relative_to_assets("m_movie.png"))
       self.m_skincare_image = PhotoImage(file=self.relative_to_assets("m_skincare.png"))
       self.m_coffe_image = PhotoImage(file=self.relative_to_assets("m_coffe.png"))
       self.m_diff_activity_image = PhotoImage(file=self.relative_to_assets("m_diff_activity.png"))
       self.m_date_image = PhotoImage(file=self.relative_to_assets("m_date.png"))
       self.m_celebration_image = PhotoImage(file=self.relative_to_assets("m_celebration.png"))
       self.m_greatful_image = PhotoImage(file=self.relative_to_assets("m_greatful.png"))
       self.m_comflic_image = PhotoImage(file=self.relative_to_assets("m_comflic.png"))
       self.m_broken_image = PhotoImage(file=self.relative_to_assets("m_broken.png"))
       self.m_diff_relationship_image = PhotoImage(file=self.relative_to_assets("m_diff_relationship.png"))
       self.m_overnight_image = PhotoImage(file=self.relative_to_assets("m_overnight.png"))
       self.m_under_four_image = PhotoImage(file=self.relative_to_assets("m_under_four.png"))
       self.m_fourtosix_image = PhotoImage(file=self.relative_to_assets("m_fourtosix.png"))
       self.m_sixtoeight_image = PhotoImage(file=self.relative_to_assets("m_sixtoeight.png"))
       self.m_above_eight_image = PhotoImage(file=self.relative_to_assets("m_above_eight.png"))


       self.m_image_added_01_image = PhotoImage(file=self.relative_to_assets("m_image_added_01.png"))
       self.m_image_added_02_image = PhotoImage(file=self.relative_to_assets("m_image_added_02.png"))
       self.m_image_added_03_image = PhotoImage(file=self.relative_to_assets("m_image_added_03.png"))
       self.m_notion_text_image = PhotoImage(file=self.relative_to_assets("m_notion_text.png"))


   def create_widgets(self):
       self.canvas.create_image(635.0,1447.0,image=self.m_jounalframeimage_image)


       self.create_mood_buttons()
       self.create_event_buttons()
       self.create_sleeping_time_buttons()
       self.create_image_added_buttons()
       self.create_note_entry()


   def create_note_entry(self):
       self.entry_bg_1 = self.canvas.create_image(639.5,2342.0,image=self.m_notion_text_image)


       # Tạo Text Widget (thay Entry) để hỗ trợ nhiều dòng + scrollbar
       self.m_notion_text = tk.Text(
           self.parent,
           bd=0,
           bg="#FFFFFF",
           font=("Crimson Pro SemiBold", 23),
           fg="#000716",
           highlightthickness=0,
           wrap="word",  # Xuống dòng tự động
           height=5,  # Số dòng hiển thị ban đầu
           width=50  # Số ký tự mỗi dòng
       )
       self.m_notion_text.place(x=96.0, y=2284.0, width=1087.0, height=114.0)


       # Tạo Scrollbar dọc
       self.scrollbar = tk.Scrollbar(self.parent, command=self.m_notion_text.yview)
       self.scrollbar.place(x=1185, y=2284, height=114)  # Vị trí scrollbar bên phải Text
       self.m_notion_text.config(yscrollcommand=self.scrollbar.set)


       # Thêm nhãn hiển thị số ký tự nhập
       self.char_count_label = tk.Label(self.parent, text="0/300", font=("Crimson Pro SemiBold", 14), fg="gray", bg="white")
       self.char_count_label.place(x=1113, y=2368)  # Vị trí gần Entry


       # Gọi hàm giới hạn ký tự từ `effect.py`
       limit_text_input(self.m_notion_text, self.char_count_label, max_length=300)
   def create_mood_buttons(self):
       """Tạo button cho mood (chỉ chọn 1 nút trong nhóm)."""
       mood_buttons = {
           "angry": (930.0, 100.74464416503906),
           "depressed": (766.0, 100.74464416503906),
           "sad": (602.0, 100.74464416503906),
           "normal": (437.0, 100.74464416503906),
           "happy": (272.0, 99.0),
       }
       for name, (x, y) in mood_buttons.items():
           create_toggle_button(self.parent, name, x, y, lambda n=name: self.add_mood(n),
                                self.button_states, "mood", )


   def add_mood(self, mood):
       self.m_mood.append(mood)

   def create_event_buttons(self):
       """Tạo button cho event (cho phép chọn nhiều nút)."""
       event_buttons = {
           "friend": (178.0, 360.0),
           "family": (342.0, 360.0),
           "crush": (507.0, 360.0),
           "ny": (671.0, 360.0),
           "coworker": (835.0, 359.0),
           "diff_people": (998.0, 359.0),
           "sunny": (178.0, 655.0),
           "rainny": (342.0, 655.0),
           "cloud": (507.0, 655.0),
           "cool": (671.0, 655.0),
           "hot": (835.0, 654.0),
           "diff_weather": (998.0, 654.0),
           "home": (179.0, 960.0),
           "study": (343.0, 960.0),
           "work": (508.0, 960.0),
           "eating": (672.0, 960.0),
           "shopping": (836.0, 959.0),
           "travel": (999.0, 959.0),
           "hospital": (178.0, 1110.0),
           "clean": (342.0, 1110.0),
           "movie": (507.0, 1110.0),
           "skincare": (671.0, 1110.0),
           "coffe": (835.0, 1109.0),
           "diff_activity": (998.0, 1109.0),
           "date": (175.0, 1403.0),
           "celebration": (339.0, 1403.0),
           "greatful": (504.0, 1403.0),
           "comflic": (668.0, 1403.0),
           "broken": (832.0, 1402.0),
           "diff_relationship": (995.0, 1402.0),
       }
       for name, (x, y) in event_buttons.items():
           create_toggle_button(self.parent, name, x, y, lambda n=name: self.add_event(n),
                                self.button_states, "event")


   def add_event(self, event):
       self.m_event.append(event)


   def create_sleeping_time_buttons(self):
       """Tạo button cho sleeping time (chỉ chọn 1 nút trong nhóm)."""
       sleeping_time_buttons = {
            "overnight": (931.0,1695.74462890625),
            "under_four": (767.0,1695.74462890625),
            "fourtosix": (603.0, 1695.74462890625),
            "sixtoeight": (438.0, 1695.74462890625),
            "above_eight": (273.0, 1694.0),
       }
       for name, (x, y) in sleeping_time_buttons.items():
           create_toggle_button(self.parent, name, x, y, lambda n=name: self.add_sleeping_time(n),
                                self.button_states, "sleeping_time")


   def add_sleeping_time(self, sleeping_time):
       self.m_sleeping_time.append(sleeping_time)


   def add_image(self, button_index):
       # Mở hộp thoại chọn file
       file_path = filedialog.askopenfilename(title="Select an Image",filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])


       if file_path:
           try:
               # Mở hình ảnh bằng PIL và resize nó để phù hợp với kích thước nút
               image = Image.open(file_path)
               image = image.resize((96, 93), Image.Resampling.LANCZOS)  # Resize ảnh
               photo_image = ImageTk.PhotoImage(image)


               # Lưu hình ảnh vào danh sách selected_images
               self.selected_images[button_index - 1] = (file_path, photo_image)


               # Hiển thị hình ảnh trên nút tương ứng
               if button_index == 1:
                   self.m_image_added_01.config(image=photo_image)
                   self.m_image_added_01.image = photo_image  # Lưu tham chiếu
               elif button_index == 2:
                   self.m_image_added_02.config(image=photo_image)
                   self.m_image_added_02.image = photo_image  # Lưu tham chiếu
               elif button_index == 3:
                   self.m_image_added_03.config(image=photo_image)
                   self.m_image_added_03.image = photo_image  # Lưu tham chiếu


           except Exception:
               pass
   def create_image_added_buttons(self):
       self.m_image_added_01 = Button(
           self.parent,
           image=self.m_image_added_01_image,
           borderwidth=0,
           highlightthickness=0,
           command=lambda: self.add_image(1),  # Thay đổi để chọn hình ảnh từ máy tính
           relief="flat")
       self.m_image_added_01.place(
           x=422.0,
           y=1999.0,
           width=96.0,
           height=93.0)


       self.m_image_added_02 = Button(
           self.parent,
           image=self.m_image_added_02_image,
           borderwidth=0,
           highlightthickness=0,
           command=lambda: self.add_image(2),  # Thay đổi để chọn hình ảnh từ máy tính
           relief="flat")
       self.m_image_added_02.place(
           x=587.0,
           y=1999.0,
           width=96.0,
           height=93.0)


       self.m_image_added_03 = Button(
           self.parent,
           image=self.m_image_added_03_image,
           borderwidth=0,
           highlightthickness=0,
           command=lambda: self.add_image(3),  # Thay đổi để chọn hình ảnh từ máy tính
           relief="flat")
       self.m_image_added_03.place(
           x=752.0,
           y=1998.0,
           width=96.0,
           height=93.0)


       # Danh sách để lưu trữ hình ảnh được chọn
       self.selected_images = [None, None, None]  # 3 vị trí cho 3 nút

   def save_data(self):
       # Đường dẫn thư mục lưu ảnh (tuyệt đối)
       username = self.controller.get_user()
       image_save_dir = base_dir/"Data" / "A_User" / f"{username}_imgs"
       os.makedirs(image_save_dir, exist_ok=True)  # Tạo thư mục nếu chưa có
       # Đường dẫn file JSON (tuyệt đối)
       json_file_path = base_dir/"Data" / "A_User" / f"{username}.json"

       # Tạo file JSON nếu chưa tồn tại
       if not os.path.exists(json_file_path):
           with open(json_file_path, "w", encoding="utf-8") as file:
               json.dump([], file, indent=4, ensure_ascii=False)

       # Lấy thời gian hiện tại
       current_time = datetime.now()
       date_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

       # Kiểm tra danh sách ảnh
       if not self.selected_images:
           return

       saved_image_names = []

       # Lưu từng hình ảnh và chuyển đổi sang PNG
       for index, item in enumerate(self.selected_images):
           if item:
               file_path, _ = item
               if os.path.exists(file_path):  # Kiểm tra file có tồn tại không
                   try:
                       # Mở ảnh bằng PIL
                       image = Image.open(file_path)

                       # Chuyển đổi sang chế độ RGB nếu cần thiết
                       if image.mode in ('RGBA', 'LA'):
                           # Tạo nền trắng cho ảnh trong suốt
                           background = Image.new('RGB', image.size, (255, 255, 255))
                           background.paste(image, mask=image.split()[-1])  # Dùng kênh alpha làm mask
                           image = background
                       elif image.mode != 'RGB':
                           image = image.convert('RGB')

                       # Tạo tên file mới với định dạng .png
                       new_file_name = f"{username}_{index + 1}_{current_time.day}_{current_time.month}_{current_time.year}.png"
                       new_file_path = os.path.join(image_save_dir, new_file_name)

                       # Lưu ảnh dưới dạng PNG
                       image.save(new_file_path, "PNG")
                       saved_image_names.append(new_file_name)
                   except Exception :
                      pass
               else:
                   pass

       # Đọc dữ liệu JSON cũ
       existing_data = []
       if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
           try:
               with open(json_file_path, "r", encoding="utf-8") as file:
                   existing_data = json.load(file)
           except json.JSONDecodeError:
               existing_data = []

       # Thêm dữ liệu mới vào JSON
       new_entry = {
           "date": date_str,
           "mood": self.m_mood[-1] if self.m_mood else "",
           "event": self.m_event,
           "sleeping_time": self.m_sleeping_time[-1] if self.m_sleeping_time else "",
           "note": self.m_notion_text.get("1.0", "end-1c"),
           "image_added": saved_image_names
       }

       existing_data.append(new_entry)

       # Ghi lại toàn bộ dữ liệu vào file JSON
       with open(json_file_path, "w", encoding="utf-8") as file:
           json.dump(existing_data, file, ensure_ascii=False, indent=4)
           file.flush()
           os.fsync(file.fileno())


class Frame06(tk.Frame):
   def __init__(self, parent, controller):
       tk.Frame.__init__(self, parent)
       self.controller = controller
       self.configure(bg="#FFFFFF")
       self.ASSETS_PATH = base_dir / "Frame" / "frame_06" / "asset_frame_06"

       # Main frame
       self.main_frame = Frame(self, bg="#6592AD")
       self.main_frame.pack(fill="both", expand=True)


       # Canvas và Scrollbar
       self.canvas = Canvas(self.main_frame, bg="#6592AD", height=1024, width=1440, highlightthickness=0)
       self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
       self.scrollbar.pack(side="right", fill="y")
       self.canvas.pack(side="left", fill="both", expand=True)
       self.canvas.configure(yscrollcommand=self.scrollbar.set)


       # Inner frame chứa JournalFrame
       self.inner_frame = Frame(self.canvas)
       self.canvas.create_window((70, 200), window=self.inner_frame, anchor="nw")


       # Thêm JournalFrame vào inner_frame
       self.journal_frame = JournalFrame(self.inner_frame, self.controller)



       self.inner_frame.bind("<Configure>", self.update_scrollregion)


       # Ảnh nền
       self.canvas.place(x=0, y=0)
       self.m_bgimage_image = PhotoImage(file=self.relative_to_assets("m_bgimage.png"))
       self.m_bgimage = self.canvas.create_image(720.0, 512.0, image=self.m_bgimage_image)


       # Hiển thị ngày tháng
       # Lấy ngày hiện tại
       now = datetime.now()


       days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


       # Lấy thứ hiện tại (lưu ý: Monday = 0, Sunday = 6)
       thu = days[now.weekday()]


       # Tạo chuỗi ngày tháng
       self.hp_daynyear_lb = f"{thu}, ngày {now.day} tháng {now.month} năm {now.year}"
       self.hp_daynyear_lb_show = self.canvas.create_text(
           0, 65.0, anchor="center", text=self.hp_daynyear_lb, justify="center",
           fill="#000000", font=("Crimson Pro SemiBold", 40 * -1)
       )
       self.canvas.bind("<Configure>", self.update_text_position)


       # Nút quay về Homepage
       self.backhp_button_image = PhotoImage(file=self.relative_to_assets("backhp_button.png"))
       self.backhp_button = Button(
           self, image=self.backhp_button_image, borderwidth=0, highlightthickness=0,
           command=lambda: self.controller.show_frame("Frame04"),
           relief="flat"
       )
       self.backhp_button.place(x=37.0, y=30.0, width=37.0, height=38.0)


       # Footer
       self.footer_frame = Frame(self, bg="#000000", height=200)
       self.footer_frame.pack(side="bottom", fill="x")
       self.footer_top = Frame(self.footer_frame, bg="#FFFFFF", height=7)
       self.footer_top.pack(fill="x")
       self.footer_bottom = Frame(self.footer_frame, bg="#000000", height=150)
       self.footer_bottom.pack(fill="x")


       # Nút đặt lại dữ liệu
       self.m_reset_image = PhotoImage(file=self.relative_to_assets("m_reset.png"))
       self.m_reset = Button(
           self.footer_bottom, image=self.m_reset_image, borderwidth=0, highlightthickness=0,
           command=lambda: print(""), relief="flat"
       )
       self.m_reset.place(x=178.0, y=10.0, width=405.0, height=76.0)


       # Nút lưu dữ liệu
       self.m_savedata_image = PhotoImage(file=self.relative_to_assets("m_savedata.png"))
       self.m_savedata = Button(
           self.footer_bottom, image=self.m_savedata_image, borderwidth=0, highlightthickness=0,
           command=self.save_data_if_valid,  # Gắn hàm save_data vào đây
           relief="flat"
       )
       self.m_savedata.place(x=636.0, y=10.0, width=735.0, height=76.0)
       self.m_savedata.place(x=636.0, y=10.0, width=735.0, height=76.0)


   def update_scrollregion(self, event):
       self.canvas.configure(scrollregion=self.canvas.bbox("all"))


   def update_text_position(self, event):
       self.canvas.coords(self.hp_daynyear_lb_show, event.width // 2, 65.0)


   def relative_to_assets(self, path: str) -> Path:
       return self.ASSETS_PATH/Path(path)

   def check_mood_sleeping_selected(self):
       """Kiểm tra nếu chưa chọn mood hoặc sleeping_time thì báo lỗi, nếu hợp lệ thì lưu"""
       selected_mood = any(btn.is_selected for btn in self.journal_frame.button_states["mood"].values())
       selected_sleeping = any(btn.is_selected for btn in self.journal_frame.button_states["sleeping_time"].values())

       if not selected_mood:
           Qmess_trackmooddi.show_window()
           return False  # Không cho phép lưu

       if not selected_sleeping:
           Qmess_trackmooddi.show_window()
           return False  # Không cho phép lưu

       return True  # Chỉ trả về True khi cả hai đều đã chọn

   def save_data_if_valid(self):
       """Chỉ lưu dữ liệu nếu người dùng đã chọn mood và sleeping_time"""
       json_file_path = base_dir /"Data"/ "A_User" /f"{self.controller.get_user()}.json"

       if self.check_and_handle_json(json_file_path):
           return
#có hàm timestammpe thì chạy không được

       # Kiểm tra nếu mood và sleeping_time đã được chọn
       if self.check_mood_sleeping_selected():
           self.journal_frame.save_data()
           self.controller.show_frame("Frame04")  # Chuyển qua Frame 4


   def check_and_handle_json(self, json_file_path):
       today = datetime.today().strftime('%Y-%m-%d')  # Lấy ngày hiện tại

       if not os.path.exists(json_file_path):
           # Tạo file JSON mới nếu không tồn tại
           with open(json_file_path, "w", encoding="utf-8") as file:
               json.dump([], file, indent=4, ensure_ascii=False)

       try:
           with open(json_file_path, 'r', encoding="utf-8") as f:
               data = json.load(f)  # Load dữ liệu
       except json.JSONDecodeError:
           # Nếu có lỗi trong việc đọc dữ liệu JSON, cho phép lưu
           return False

           # Kiểm tra xem hôm nay có dữ liệu chưa
       if any(entry.get("date").startswith(today) for entry in data):
           Qmess_checkdulieu.show_window()
           return True  # Có dữ liệu đã tồn tại
       return False  # Không tồn tại dữ liệu nào
#thiếu hàm timestamp thì chạy không được
   
