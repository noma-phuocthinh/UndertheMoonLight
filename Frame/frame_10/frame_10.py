from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Scrollbar, Text
from PIL import Image, ImageTk

from Function.effect import round_corners


base_dir = Path(__file__).parents[2]
IMAGE_FOLDER = base_dir / "Data" / "Tarot" / "data_tarot_image"

def relative_to_assets(path: str) -> Path:
    return base_dir/ "Frame"/"frame_10"/"asset_frame_10" / Path(path)

def relative_to_data(path: str) -> Path:
    return IMAGE_FOLDER/ Path(path)


class Frame10(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_card_image = None  # Để giữ ảnh hiện tại

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
        # Hình nền chính
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(720.0, 512.0, image=self.image_image_1)

        self.text_id = self.canvas.create_text(
            720,  # Trung tâm của 1440
            65.0,  # Y giữ nguyên
            anchor="center",  # Căn giữa theo tâm
            text=self.controller.format_date(),
            fill="#FFFFFF",
            font=("Crimson Pro Bold", 40 * -1)
        )

        #Vùng hiển thị lá bài
        self.tarot_card_lb = self.canvas.create_image(283.0, 546.0)
        # Scrollbar và Text Widget
        self.text_scrollbar = Scrollbar(self, orient="vertical")
        self.tarot_text = Text(
            self,
            wrap="word",
            font=("Crimson Pro Regular", 20),
            bg="#000000",  # Màu nền tối (tùy chỉnh)
            fg="#F5E1FD",  # Chữ màu trắng
            height=50,  # Giới hạn chiều cao (tùy chỉnh)
            width=40,  # Chiều rộng (tùy chỉnh)
            yscrollcommand=self.text_scrollbar.set
        )
        self.text_scrollbar.config(command=self.tarot_text.yview)

        # Vị trí hiển thị
        self.tarot_text.place(x=524, y=203, width=820, height=686)
        self.text_scrollbar.place(x=524, y=203, height=686)

        #Nút quay lại Frame04
        self.backhp_button_image = PhotoImage(file=relative_to_assets("backhp_button.png"))
        self.backhp_button = Button(
            self,
            image=self.backhp_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: controller.show_frame("Frame04"),
            relief="flat"
        )
        self.backhp_button.place(x=41.0, y=33.0, width=36.0, height=37.0)

    def update_tarot_card(self, card):
        """Cập nhật hình ảnh và nội dung lá bài Tarot được chọn."""
        # Sử dụng hàm relative_to_assets để lấy đường dẫn ảnh tương đối
        image_path = relative_to_data(card.get("Hình ảnh", ""))
        print("DEBUG: ", image_path)

        # Cập nhật hình ảnh lá bài
        if image_path.exists():  # Kiểm tra xem ảnh có tồn tại không
            img = Image.open(image_path).resize((350, 650), Image.LANCZOS)
            img = round_corners(img, radius=50)
            self.current_card_image = ImageTk.PhotoImage(img)
            self.canvas.itemconfig(self.tarot_card_lb, image=self.current_card_image)
        else:
            self.canvas.itemconfig(self.tarot_card_lb, image=None)

        # Cập nhật nội dung trong Text Widget
        text_content = f"Tên lá bài: {card.get('Tên lá bài', 'Không có tên')}\n\n"
        text_content += f"Từ khóa: {card.get('Từ khóa', 'Không có từ khóa')}\n\n"
        text_content += f"Ý nghĩa:\n{card.get('Ý nghĩa xuôi', 'Không có ý nghĩa')}"

        self.tarot_text.config(state="normal")  # Cho phép chỉnh sửa
        self.tarot_text.delete("1.0", tk.END)  # Xóa nội dung cũ
        self.tarot_text.insert("1.0", text_content)  # Thêm nội dung mới
        self.tarot_text.config(state="disabled")  # Khóa lại tránh chỉnh sửa
