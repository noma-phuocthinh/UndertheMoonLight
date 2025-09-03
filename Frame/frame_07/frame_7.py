from mutagen.mp3 import MP3
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import json
from datetime import datetime
import pygame
import time
from Function.Music.journalentry import JournalEntry
from PIL import Image, ImageTk
from Qmess.qmess_warning.ms_Qmess_nhatkydi import Qmess_nhatkydi
from Function.effect import create_fav_button, MarqueeText, truncate_text, round_corners
import random


base_dir = Path(__file__).parents[2]



def relative_to_assets(path: str) -> Path:
    return base_dir/"Frame"/ "frame_07" / "asset_frame_07" / Path(path)


class Frame07(tk.Frame):  # Tạo lớp Frame07 kế thừa từ tk.Frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Khởi tạo pygame mixer
        pygame.mixer.init()
        # Danh sách button nhạc
        self.music_buttons = []
        self.list5 = []
        self.is_playing = False  # Trạng thái nhạc đang phát hay không
        self.is_looping = False  # Trạng thái loop nhạc
        self.current_song_index = 0 # Chỉ số bài hát thực trong danh sách
        self.current_playing_index = 0  # Chỉ số bài hát đang phát (random)
        self.check_music_event()
        # Đăng ký sự kiện khi nhạc kết thúc
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.master.bind("<<MusicEnd>>", self.loop_music)

        # Gọi update_display để cập nhật danh sách bài hát
        songs = self.update_display()
        if songs:
            self.list5 = songs
        else:
            pass

        # Gọi hàm tạo text và nút nhạc sau khi cập nhật list5
        self.create_music_texts()
        self.create_music_buttons(self.list5)
        # Đặt ảnh mặc định khi khởi tạo
        self.reset_image()


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

        # Nút fav_library
        self.ms_fav_library_image = PhotoImage(file=relative_to_assets("ms_fav_library.png"))
        self.ms_fav_library = Button(
            self,
            image=self.ms_fav_library_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print(""),
            relief="flat"
        )
        self.ms_fav_library.place(x=22.0, y=157.0, width=100.0, height=100.0)

        # Nút rec_library
        self.ms_rec_library_image = PhotoImage(file=relative_to_assets("ms_rec_library.png"))
        self.ms_rec_library = Button(
            self,
            image=self.ms_rec_library_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print(""),
            relief="flat"
        )
        self.ms_rec_library.place(x=22.0, y=736.0, width=100.0, height=100.0)

        # Nút backmusic
        self.ms_backmusic_image = PhotoImage(file=relative_to_assets("ms_backmusic.png"))
        self.ms_backmusic = Button(
            self,
            image=self.ms_backmusic_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.back_music,  # Gọi hàm back_music khi nhấn
            relief="flat"
        )
        self.ms_backmusic.place(x=1083.0, y=774.0, width=22.0, height=22.0)

        # Nút nextmusic
        self.ms_nextmusic_image = PhotoImage(file=relative_to_assets("ms_nextmusic.png"))
        self.ms_nextmusic = Button(
            self,
            image=self.ms_nextmusic_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.next_music,  # Gọi hàm next_music khi nhấn
            relief="flat"
        )
        self.ms_nextmusic.place(x=1258.0, y=774.0, width=21.0, height=21.0)

        # Load và hiển thị hình ảnh
        self.ms_backgr_image = PhotoImage(file=relative_to_assets("ms_backgr.png"))
        self.ms_backgr = self.canvas.create_image(720.0, 512.0, image=self.ms_backgr_image)

        # Load và hiển thị hình ảnh mặc định (màu trắng)
        self.ms_big_white_pic_image = PhotoImage(file=relative_to_assets("ms_big_white_pic.png"))
        self.ms_big_white_pic = self.canvas.create_image(1173.0, 337.0, image=self.ms_big_white_pic_image)
        # Thứ ngày
        self.canvas.create_text(
            175.0,
            43.0,
            anchor="nw",
            text=self.controller.format_date(),
            fill="#FFFFFF",
            font=("Crimson Pro SemiBold", 40 * -1)
        )
        # Nút backhp_button
        self.backhp_button_image = PhotoImage(file=relative_to_assets("backhp_button.png"))

        self.backhp_button = Button(
            self,
            image=self.backhp_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: [self.reset_music_state(), self.controller.show_frame("Frame04")],
            relief="flat"
        )

        self.backhp_button.place(x=38.0, y=31.0, width=36.0, height=37.0)
        # Thêm các text vào canvas
        self.canvas.create_text(
            201.0,
            151.0,
            anchor="nw",
            text="Âm nhạc là liều thuốc của tâm hồn",
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 32)
        )
        self.canvas.create_text(
            201.0,
            197.0,
            anchor="nw",
            text="Chúng mình ở đây để giúp bạn đắm chìm trong âm nhạc",
            fill="#FFFFFF",
            font=("Crimson Pro Regular", 23)
        )

        # Load hình ảnh cho nút favmusic5
        self.ms_favmusic5_image = PhotoImage(file=relative_to_assets("ms_favmusic5.png"))
        self.ms_favmusic5_clicked_image = PhotoImage(
            file=relative_to_assets("ms_favmusic5_clicked.png"))  # Ảnh khi nhấn

        # Tạo nút với hiệu ứng đổi ảnh khi nhấn
        self.ms_favmusic5 = create_fav_button(
            parent=self,
            x=786, y=797, width=41, height=37,  # Giữ nguyên vị trí cũ
            img_default=self.ms_favmusic5_image,
            img_clicked=self.ms_favmusic5_clicked_image,
            command=lambda: print("")  # Hành động khi nhấn
        )
        # Load hình ảnh cho nút favmusic4
        self.ms_favmusic4_image = PhotoImage(file=relative_to_assets("ms_favmusic4.png"))
        self.ms_favmusic4_clicked_image = PhotoImage(
            file=relative_to_assets("ms_favmusic4_clicked.png"))  # Ảnh khi nhấn

        # Tạo nút với hiệu ứng đổi ảnh khi nhấn
        self.ms_favmusic4 = create_fav_button(
            parent=self,
            x=786, y=671, width=41, height=37,  # Giữ nguyên vị trí cũ
            img_default=self.ms_favmusic4_image,
            img_clicked=self.ms_favmusic4_clicked_image,
            command=lambda: print("")  # Hành động khi nhấn
        )

        # Load hình ảnh cho nút favmusic3
        self.ms_favmusic3_image = PhotoImage(file=relative_to_assets("ms_favmusic3.png"))
        self.ms_favmusic3_clicked_image = PhotoImage(
            file=relative_to_assets("ms_favmusic3_clicked.png"))  # Ảnh khi nhấn

        # Tạo nút với hiệu ứng đổi ảnh khi nhấn
        self.ms_favmusic3 = create_fav_button(
            parent=self,
            x=787, y=544, width=40, height=36,  # Giữ nguyên vị trí cũ
            img_default=self.ms_favmusic3_image,
            img_clicked=self.ms_favmusic3_clicked_image,
            command=lambda: print("")  # Hành động khi nhấn
        )

        # Load hình ảnh cho nút favmusic2
        self.ms_favmusic2_image = PhotoImage(file=relative_to_assets("ms_favmusic2.png"))
        self.ms_favmusic2_clicked_image = PhotoImage(
            file=relative_to_assets("ms_favmusic2_clicked.png"))  # Ảnh khi nhấn

        # Tạo nút với hiệu ứng đổi ảnh khi nhấn
        self.ms_favmusic2 = create_fav_button(
            parent=self,
            x=787, y=420, width=40, height=36,  # Thay đổi x, y nếu cần
            img_default=self.ms_favmusic2_image,
            img_clicked=self.ms_favmusic2_clicked_image,
            command=lambda: print("")  # Hành động khi nhấn
        )

        self.ms_favmusic1_image = PhotoImage(file=relative_to_assets("ms_favmusic1.png"))
        self.ms_favmusic1_clicked_image = PhotoImage(
            file=relative_to_assets("ms_favmusic1_clicked.png"))  # Ảnh khi nhấn

        # Tạo nút với hiệu ứng đổi ảnh khi nhấn
        self.ms_favmusic1 = create_fav_button(
            parent=self,
            x=787, y=289, width=40, height=36,
            img_default=self.ms_favmusic1_image,
            img_clicked=self.ms_favmusic1_clicked_image,
            command=lambda: print("")  # Hành động khi nhấn
        )
        # Nút play/stop music
        self.ms_playmusic_image = PhotoImage(file=relative_to_assets("ms_playmusic.png"))
        self.ms_playmusic = Button(
            self,
            image=self.ms_playmusic_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.toggle_music,
            relief="flat"
        )
        self.ms_playmusic.place(x=1139.0, y=742.0, width=84.0, height=84.0)
        # Nút random music
        self.ms_randommusic_image = PhotoImage(file=relative_to_assets("ms_randommusic.png"))
        self.ms_randommusic = Button(
            self,
            image=self.ms_randommusic_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.random_music,  # Gọi hàm phát nhạc ngẫu nhiên
            relief="flat"
        )
        self.ms_randommusic.place(x=1018.0, y=769.0, width=31.0, height=31.0)
        # Nút loop music
        self.ms_loopmusic_image = PhotoImage(file=relative_to_assets("ms_loopmusic.png"))
        self.ms_loopmusic = Button(
            self,
            image=self.ms_loopmusic_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.toggle_loop,  # Gọi hàm bật/tắt loop
            relief="flat"
        )
        self.ms_loopmusic.place(x=1313.0, y=769.0, width=25.0, height=29.0)

        self.slider = tk.Scale(
            self,
            from_=0,
            to=1000,
            orient=tk.HORIZONTAL,
            sliderlength=15,
            showvalue=0,
            troughcolor='#4A4A4A',
            bg='#2B2B2B',
            highlightthickness=0,
            borderwidth=0
        )
        self.slider.place(x=966, y=855, width=424, height=10)

        # Biến trạng thái
        self.is_slider_dragging = False
        self.song_length = 0  # Thời lượng bài hát (giây)
        self.slider_update_id = None

        # Bind sự kiện
        self.slider.bind("<ButtonPress-1>", self.start_drag)
        self.slider.bind("<B1-Motion>", self.on_drag)
        self.slider.bind("<ButtonRelease-1>", self.end_drag)

        self.is_seeking = False

        self.start_time = 0  # Thời điểm bắt đầu phát
        self.paused_time = 0  # Thời gian đã tạm dừng
        self.song_length = 0  # Tổng thời lượng bài hát
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)  # Sử dụng event riêng
        self.master.bind("<<MusicFinished>>", self.handle_music_end)
        self.force_loop_check()
        self.check_music_event()

    def reset_image(self):
        """Đặt lại ảnh mặc định là màu trắng."""
        try:
            white_image_path = relative_to_assets("ms_big_white_pic.png")  # Ảnh trắng mặc định
            white_image = Image.open(white_image_path).resize((450, 450), Image.LANCZOS)
            white_image = round_corners(white_image,30)
            self.ms_big_white_pic_image = ImageTk.PhotoImage(white_image)

            # Cập nhật ảnh trên canvas
            self.canvas.itemconfig(self.ms_big_white_pic, image=self.ms_big_white_pic_image)
        except Exception:
            pass

    def update_song_image(self, image_path):
        """Cập nhật hình ảnh bài hát"""
        try:
            # Tạo ảnh mới từ đường dẫn
            new_image = Image.open(image_path)
            resized_image = new_image.resize((450, 450), Image.LANCZOS)
            resized_image = round_corners(resized_image,30)# Resize ảnh nếu cần
            tk_image = ImageTk.PhotoImage(resized_image)

            # Cập nhật lại ảnh trong canvas
            self.canvas.itemconfig(self.ms_big_white_pic, image=tk_image)

            # Lưu ảnh vào thuộc tính để tránh bị giải phóng bộ nhớ
            self.current_image = tk_image
        except Exception as e:
            pass

    def update_display(self):
        """Cập nhật danh sách bài hát dựa trên mood hiện tại."""
        today = datetime.today()
        dd, mm, yy = today.day, today.month, today.year
        self.user = self.controller.get_user()
        if not self.user:
            return []
        js = base_dir / "Data"/"A_User" / f"{self.user}.json"

        entries = []
        if js.exists():
            try:
                with open(js, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    entries = [
                        JournalEntry(entry["date"], entry["mood"], entry["event"], entry["note"], entry["image_added"])
                        for entry in data
                    ]
            except Exception :
                return []

        target_date = datetime(yy, mm, dd).strftime("%Y-%m-%d")
        mood_curr = None

        for entry in entries:
            try:
                entry_date = datetime.strptime(entry.date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                if entry_date == target_date:
                    mood_curr = entry.mood
                    break
            except Exception :
                continue

        if mood_curr is None:
            # Chỉ gọi Qmess_nhatkydi nếu frame này đang hiển thị
            if self.winfo_ismapped():
                self.after(500, lambda: Qmess_nhatkydi.show_window(
                    parent=self,
                    controller=self.controller  # Truyền controller vào
                ))

            return []

        json_file_path = base_dir /"Data"/ "Music" / "data_music_sorted.json"
        try:
            with open(json_file_path, 'r', encoding="utf-8") as file:
                songs = json.load(file)
        except Exception :
            return []

        if mood_curr in songs:
            mood_songs = songs[mood_curr]
            selected_songs = random.sample(mood_songs, min(len(mood_songs), 5))
            return selected_songs
        else:
            # Chỉ gọi Qmess_nhatkydi nếu frame này đang hiển thị
            if self.winfo_ismapped():
                self.after(500, lambda: Qmess_nhatkydi.show_window(
                    parent=self,
                    controller=self.controller  # Truyền controller vào
                ))

            return []


    def create_music_buttons(self, songs):
        """Tạo các nút nhạc dựa trên danh sách bài hát."""

        # Khởi tạo danh sách các nút nếu chưa có
        if not hasattr(self, 'music_buttons'):
            self.music_buttons = []

        # Xóa các nút nhạc cũ nếu có
        for button in self.music_buttons:
            button.destroy()
        self.music_buttons.clear()

        button_positions = [
            (201, 257),  # Vị trí nút 1
            (202, 391),  # Vị trí nút 2
            (202, 512),  # Vị trí nút 3
            (202, 640),  # Vị trí nút 4
            (202, 767)  # Vị trí nút 5
        ]

        # Khởi tạo danh sách giữ ảnh (nếu chưa có)
        if not hasattr(self, 'images'):
            self.images = []

        # Giới hạn số nút không vượt quá số vị trí cho phép
        max_buttons = min(len(songs), len(button_positions))

        for i in range(max_buttons):
            song = songs[i]
            try:
                # Tạo đường dẫn ảnh từ tên file
                image_path = base_dir /"Data"/ "Music" / "DATA_IMAGE" / song['Music Image']

                pil_image = Image.open(image_path)
                resized_image = pil_image.resize((100, 100), Image.LANCZOS)  # Resize ảnh
                image = ImageTk.PhotoImage(resized_image)

                # Giữ tham chiếu vào danh sách ảnh
                self.images.append(image)

                def update_marquee_text(index=i, song=song):

                    # Cập nhật chỉ số bài hát hiện tại
                    self.current_song_index = index

                    self.TenBaiHat.set_text(song['Name'])
                    self.TenCaSi.set_text(song['Singer'])

                    # Đường dẫn ảnh bài hát
                    image_path = base_dir / "Data" / "Music" / "DATA_IMAGE" / song['Music Image']
                    self.update_song_image(image_path)

                    # Đường dẫn nhạc bài hát
                    self.current_music_path = base_dir / "Data" / "Music" / "DATA_MUSIC" / song['Music Path']

                    # Phát nhạc ngay khi bấm vào nút chọn nhạc
                    try:
                        pygame.mixer.music.load(self.current_music_path)
                        pygame.mixer.music.play()
                        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Đăng ký sự kiện
                        self.check_music_event()
                        self.is_playing = True  # Cập nhật trạng thái nhạc
                        self.update_play_button()  # Đổi ảnh nút sang stop
                        self.start_time = time.time()  # Cập nhật thời gian bắt đầu phát
                        self.paused_time = 0
                    except Exception :
                        pass

                    try:
                        audio = MP3(self.current_music_path)
                        self.song_length = audio.info.length

                        # Cập nhật lại slider và khởi động update_slider
                        self.slider.set(0)  # Reset thanh trượt về đầu
                        self.slider.config(to=1000)  # Đặt giá trị tối đa là 1000 (thanh trượt chuẩn)
                        if self.slider_update_id:
                            self.after_cancel(self.slider_update_id)  # Hủy cập nhật cũ nếu có
                        self.update_slider()  # Bắt đầu cập nhật slider lại
                    except Exception :
                        pass

                # Tạo nút với ảnh
                button = Button(
                    self,
                    image=image,
                    borderwidth=0,
                    highlightthickness=0,
                    command=update_marquee_text,
                    relief="flat"
                )
                button.place(x=button_positions[i][0], y=button_positions[i][1], width=100.0, height=100.0)
                self.music_buttons.append(button)
            except Exception :
                pass

    def create_music_texts(self):
        """Tạo các text hiển thị tên bài hát và ca sĩ."""

        # Kiểm tra canvas tồn tại
        if not hasattr(self, 'canvas') or self.canvas is None:
            return


        # Xóa các text cũ nếu có
        if hasattr(self, 'music_texts'):
            for text_id in self.music_texts:
                self.canvas.delete(text_id)
            self.music_texts.clear()
        else:
            self.music_texts = []

        # Vị trí các text (tên bài hát và ca sĩ)
        text_positions = [
            (322, 267),  # Tên bài hát 1
            (322, 401),  # Tên bài hát 2
            (322, 522),  # Tên bài hát 3
            (322, 650),  # Tên bài hát 4
            (322, 777),  # Tên bài hát 5
        ]

        singer_positions = [
            (323, 310),  # Ca sĩ bài hát 1
            (323, 444),  # Ca sĩ bài hát 2
            (323, 565),  # Ca sĩ bài hát 3
            (323, 693),  # Ca sĩ bài hát 4
            (323, 820),  # Ca sĩ bài hát 5
        ]

        for i, song in enumerate(self.list5):
            try:
                # Kiểm tra tính hợp lệ của từ điển bài hát
                if 'Name' not in song or 'Singer' not in song:
                    continue

                # Tạo text tên bài hát (sử dụng hàm truncate_text)
                text_id = self.canvas.create_text(
                    text_positions[i][0], text_positions[i][1],
                    anchor="nw",
                    text=truncate_text(song['Name']),
                    fill="#FFFFFF",
                    font=("Crimson Pro SemiBold", 32 * -1)
                )
                self.music_texts.append(text_id)

                # Tạo text tên ca sĩ
                singer_id = self.canvas.create_text(
                    singer_positions[i][0], singer_positions[i][1],
                    anchor="nw",
                    text=song['Singer'],
                    fill="#FFFFFF",
                    font=("Crimson Pro ExtraLight", 25 * -1)
                )
                self.music_texts.append(singer_id)

            except Exception :
                pass

        # Nếu đã tồn tại đối tượng chạy chữ, cập nhật thay vì tạo mới
        if hasattr(self, 'TenBaiHat'):
            self.TenBaiHat.set_text("Tên bài hát")
        else:
            self.TenBaiHat = MarqueeText(self.canvas, 950, 600, 1398, 650, "Tên bài hát", speed=1)

        if hasattr(self, 'TenCaSi'):
            self.TenCaSi.set_text("Tên ca sĩ")
        else:
            self.TenCaSi = MarqueeText(self.canvas, 950, 657, 1398, 707, "Tên ca sĩ", font_size=20, speed=1)

    def play_music(self):
        """Phát nhạc và reset thời gian"""
        try:
            pygame.mixer.music.load(self.current_music_path)
            pygame.mixer.music.play()
            self.start_time = time.time() - self.paused_time
            self.paused_time = 0
            self.is_playing = True
            self.update_slider()
        except Exception :
            pass

    def toggle_music(self):
        """Bật/tắt phát nhạc"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.paused_time = time.time() - self.start_time
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.start_time = time.time() - self.paused_time
            self.is_playing = True
        self.update_play_button()

    def update_play_button(self):
        """Cập nhật ảnh của nút phát/dừng nhạc."""
        if self.is_playing:
            self.ms_playmusic_image = PhotoImage(file=relative_to_assets("ms_stopmusic.png"))
        else:
            self.ms_playmusic_image = PhotoImage(file=relative_to_assets("ms_playmusic.png"))

        self.ms_playmusic.config(image=self.ms_playmusic_image)

    def random_music(self):
        """Chọn ngẫu nhiên một bài hát"""
        try:
            # Lấy một chỉ số ngẫu nhiên khác với bài hát hiện tại
            new_index = random.randint(0, len(self.list5) - 1)

            while new_index == self.current_song_index:
                new_index = random.randint(0, len(self.list5) - 1)

            # Cập nhật chỉ số bài hát hiện tại
            self.current_song_index = new_index
            random_song = self.list5[self.current_song_index]

            # Cập nhật thông tin bài hát trên giao diện
            self.TenBaiHat.set_text(random_song['Name'])
            self.TenCaSi.set_text(random_song['Singer'])

            # Đường dẫn ảnh bài hát
            image_path = base_dir / "Data" / "Music" / "DATA_IMAGE" / random_song['Music Image']
            self.update_song_image(image_path)

            # Đường dẫn nhạc bài hát
            self.current_music_path = base_dir / "Data" / "Music" / "DATA_MUSIC" / random_song['Music Path']

            # Phát nhạc
            pygame.mixer.music.load(self.current_music_path)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Đăng ký sự kiện
            self.check_music_event()
            self.is_playing = True

            # Reset thanh trượt
            self.start_time = time.time()
            self.slider.set(0)

            # Cập nhật lại slider
            if self.slider_update_id:
                self.after_cancel(self.slider_update_id)
            self.update_slider()

            self.update_play_button()
        except Exception :
            pass

    def toggle_loop(self):
        """Bật/tắt chế độ loop với cơ chế bảo vệ"""
        self.is_looping = not self.is_looping

        # Đảm bảo đăng ký sự kiện đúng cách
        if self.is_looping:
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
        else:
            pygame.mixer.music.set_endevent()

        # Cập nhật hình ảnh nút
        new_image = PhotoImage(
            file=relative_to_assets("ms_loopmusic_click.png" if self.is_looping else "ms_loopmusic.png")
        )
        self.ms_loopmusic.configure(image=new_image)
        self.ms_loopmusic.image = new_image

    def loop_music(self, event=None):
        """Phát lại bài hát khi loop được bật"""
        if self.is_looping and self.current_music_path:
            pygame.mixer.music.load(self.current_music_path)  # Load lại bài hát
            pygame.mixer.music.play()
            # Cập nhật lại thời gian bắt đầu và slider
            self.start_time = time.time()
            self.slider.set(0)

    def check_music_event(self):
        """Kiểm tra sự kiện với cơ chế lọc trùng lặp"""
        try:
            # Lấy và xử lý tất cả sự kiện trong hàng đợi
            for event in pygame.event.get(pygame.USEREVENT):
                self.handle_music_end()

            # Lên lịch kiểm tra lại sau 100ms
            self.after(100, self.check_music_event)
        except pygame.error:
            pygame.init()
            self.after(100, self.check_music_event)

    def handle_music_end(self, event=None):
        """Xử lý kết thúc bài hát với cơ chế chống loop vô hạn"""
        if self.is_looping and hasattr(self, 'current_music_path'):
            # Kiểm tra trạng thái phát nhạc thực tế
            if not pygame.mixer.music.get_busy():
                try:
                    # Tải và phát lại bài hát
                    pygame.mixer.music.load(self.current_music_path)
                    pygame.mixer.music.play()

                    # Đặt lại các thông số thời gian
                    self.start_time = time.time()
                    self.slider.set(0)
                    self.is_playing = True

                    # Đăng ký lại sự kiện kết thúc
                    pygame.mixer.music.set_endevent(pygame.USEREVENT)
                except Exception :
                    pass
            else:
                pass
        else:
            self.is_playing = False
        self.update_play_button()

    def next_music(self):
        """Phát bài hát tiếp theo"""
        try:

            # Tăng chỉ số bài hát
            self.current_song_index = (self.current_song_index + 1) % len(self.list5)
            next_song = self.list5[self.current_song_index]

            # Cập nhật thông tin bài hát trên giao diện
            self.TenBaiHat.set_text(next_song['Name'])
            self.TenCaSi.set_text(next_song['Singer'])

            # Đường dẫn ảnh bài hát
            image_path = base_dir / "Data" / "Music" / "DATA_IMAGE" / next_song['Music Image']
            self.update_song_image(image_path)

            # Đường dẫn nhạc bài hát
            self.current_music_path = base_dir / "Data" / "Music" / "DATA_MUSIC" / next_song['Music Path']

            # Phát nhạc
            pygame.mixer.music.load(self.current_music_path)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.check_music_event()
            self.is_playing = True

            # Reset thanh trượt
            self.start_time = time.time()
            self.slider.set(0)

            # Cập nhật lại slider
            if self.slider_update_id:
                self.after_cancel(self.slider_update_id)
            self.update_slider()

            self.update_play_button()
        except Exception :
            pass

    def back_music(self):
        """Quay lại bài hát trước đó"""
        try:
            self.current_song_index = (self.current_song_index - 1) % len(self.list5)
            previous_song = self.list5[self.current_song_index]

            # Cập nhật thông tin bài hát
            self.TenBaiHat.set_text(previous_song['Name'])
            self.TenCaSi.set_text(previous_song['Singer'])

            # Đường dẫn ảnh bài hát
            image_path = base_dir / "Data" / "Music" / "DATA_IMAGE" / previous_song['Music Image']
            self.update_song_image(image_path)

            # Đường dẫn nhạc bài hát
            self.current_music_path = base_dir / "Data" / "Music" / "DATA_MUSIC" / previous_song['Music Path']

            # Phát nhạc
            pygame.mixer.music.load(self.current_music_path)
            pygame.mixer.music.play()
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.check_music_event()
            self.is_playing = True

            # Reset thanh trượt
            self.start_time = time.time()
            self.slider.set(0)

            # Cập nhật lại slider
            if self.slider_update_id:
                self.after_cancel(self.slider_update_id)
            self.update_slider()

            self.update_play_button()
        except Exception :
            pass

    def start_drag(self, event):
        """Bắt đầu kéo slider"""
        self.is_slider_dragging = True
        if self.is_playing:
            pygame.mixer.music.pause()

    def on_drag(self, event):
        """Xử lý trong khi kéo slider"""
        if self.is_slider_dragging and self.song_length > 0:
            slider_width = self.slider.winfo_width()
            x = event.x
            percentage = min(max(x / slider_width, 0.0), 1.0)
            seek_pos = percentage * self.song_length
            self.slider.set((seek_pos / self.song_length) * 1000)

    def end_drag(self, event):
        """Xử lý khi người dùng thả thanh trượt"""
        if hasattr(self, 'current_music_path') and self.current_music_path:
            new_pos = self.slider.get() / 1000 * self.song_length  # Tính thời gian mới (giây)

            # Giới hạn tua không vượt quá cuối bài
            if new_pos >= self.song_length - 1:
                new_pos = self.song_length - 1

            pygame.mixer.music.fadeout(100)  # Dừng nhạc mượt hơn thay vì stop()
            time.sleep(0.1)  # Đợi một chút trước khi phát lại

            pygame.mixer.music.load(self.current_music_path)
            pygame.mixer.music.play(start=int(new_pos))  # Phát từ vị trí mới

            self.is_playing = True
            self.is_slider_dragging = False  # Đánh dấu đã tua xong
            self.start_time = time.time() - new_pos  # Cập nhật thời gian bắt đầu

            self.slider.set((new_pos / self.song_length) * 1000)  # Cập nhật thanh trượt ngay lập tức
            self.after(500, self.update_slider)  # Chắc chắn update_slider sẽ chạy
            self.update_play_button()

    def seek_music(self, position):
        """Tua đến vị trí mong muốn"""
        try:
            # Chuyển đổi vị trí slider sang giây
            seek_pos = (position / 1000) * self.song_length

            # Dừng và phát lại từ vị trí mới
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.current_music_path)
            pygame.mixer.music.play(start=int(seek_pos))

            # Cập nhật thời gian bắt đầu
            self.start_time = time.time() - seek_pos
            self.is_playing = True
        except Exception :
            pass

    def update_slider(self):
        """Cập nhật slider với kiểm tra trạng thái thực tế"""
        if self.is_playing and pygame.mixer.music.get_busy():
            current_time = time.time() - self.start_time
            progress = (current_time / self.song_length) * 1000
            self.slider.set(min(progress, 1000))
        elif self.is_playing:
            self.is_playing = False
            self.update_play_button()

        self.slider_update_id = self.after(500, self.update_slider)

    def check_music_end(self):
        """Kiểm tra nếu bài hát thực sự kết thúc"""
        if self.is_playing and not self.is_slider_dragging and not self.is_seeking:
            if not pygame.mixer.music.get_busy():
                self.after(2000, self.verify_music_end)  # Chờ 2 giây trước khi xác nhận
            else:
                self.after(1000, self.check_music_end)

    def verify_music_end(self):
        """Xác nhận lại bài hát có thực sự kết thúc hay không"""
        if self.is_playing and not self.is_slider_dragging and not self.is_seeking:
            self.after(1000, self.final_check)

    def final_check(self):
        """Kiểm tra lần cuối xem nhạc có thực sự dừng không"""
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.is_playing = False  # Cập nhật trạng thái dừng
            self.handle_music_end()
        else:
            self.check_music_end()
    def reset_seeking(self):
        """Bỏ trạng thái tua để kiểm tra kết thúc bài hát"""
        self.is_seeking = False
        self.check_music_end()

    def restart_music(self, new_pos):
        """Dừng nhạc rồi phát lại từ vị trí mới"""
        if hasattr(self, 'current_music_path') and self.current_music_path:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.current_music_path)
            pygame.mixer.music.play(start=int(new_pos))  # Phát từ vị trí mới

            self.is_playing = True  # Xác nhận trạng thái phát nhạc
            self.is_seeking = True  # Đánh dấu đang tua

            self.after(1000, self.update_slider)  # Đảm bảo cập nhật thanh trượt ngay
            self.after(1000, self.reset_seeking)  # Tránh hiểu nhầm bài hát kết thúc

    def check_pygame_event(self):
        """Xử lý sự kiện từ pygame"""
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:  # Kiểm tra sự kiện kết thúc bài hát
                self.handle_music_end()
        self.after(100, self.check_pygame_event)  # Tiếp tục kiểm tra sự kiện

    def force_loop_check(self):
        """Kiểm tra ép buộc nếu hệ thống bỏ lỡ sự kiện"""
        if self.is_looping and self.is_playing and not pygame.mixer.music.get_busy():
            self.handle_music_end()
        self.after(1000, self.force_loop_check)  # Kiểm tra mỗi giây

    def reset_music_state(self):
        """Reset trạng thái nhạc khi thoát khỏi giao diện"""
        pygame.mixer.music.stop()  # Dừng nhạc ngay lập tức
        pygame.mixer.music.unload()  # Giải phóng bộ nhớ nhạc đang phát
        self.is_playing = False  # Đánh dấu nhạc không còn phát
        self.is_looping = False  # Đặt lại trạng thái loop
        self.current_song_index = 0  # Đặt lại chỉ số bài hát
        self.current_playing_index = 0  # Đặt lại chỉ số random
        self.current_music_path = ""  # Xóa đường dẫn bài hát hiện tại
        self.slider.set(0)  # Đưa thanh trượt về đầu
        if self.slider_update_id:
            self.after_cancel(self.slider_update_id)  # Hủy cập nhật thanh trượt nếu có

        # Cập nhật giao diện nút loop về trạng thái ban đầu (nếu có)
        self.ms_loopmusic.config(image=self.ms_loopmusic_image)  # Đặt lại ảnh mặc định cho nút loop








