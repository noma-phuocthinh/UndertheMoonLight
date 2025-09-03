import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from tkinter import PhotoImage, Button
from pathlib import Path


# Hàm lấy đường dẫn ảnh từ thư mục asset
base_dir=Path(__file__).parents[1]
ASSETS_PATH = base_dir/"Frame"/"frame_06"/"asset_frame_06"

def relative_to_assets(path: str) -> Path:
   return base_dir/"Frame"/"frame_06"/"asset_frame_06"/ Path(path)

def create_hover_button(parent, x, y, width, height, img_default, img_hover, command):
    """
    Hàm tạo nút có hiệu ứng hover.
    - parent: Frame hoặc Tk window chứa nút.
    - x, y, width, height: Tọa độ và kích thước nút.
    - img_default: Ảnh mặc định.
    - img_hover: Ảnh khi hover.
    - command: Hàm sẽ gọi khi bấm vào nút.
    """
    button = tk.Button(
        parent,
        image=img_default,
        command=command,
        relief="flat"
    )
    button.place(x=x, y=y, width=width, height=height)

    # Gán sự kiện hover
    button.bind("<Enter>", lambda e: button.config(image=img_hover))
    button.bind("<Leave>", lambda e: button.config(image=img_default))

    return button


def round_corners(image, radius):
    """Bo góc ảnh với bán kính `radius`"""
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius, fill=255)
    image.putalpha(mask)  # Áp dụng mặt nạ bo góc
    return image


def create_rounded_corner_avatar(image_path, size, radius):
    """Resize và bo góc ảnh từ `image_path` với kích thước `size` và bán kính `radius`."""
    image = Image.open(image_path).convert("RGBA")  # Đảm bảo có kênh alpha
    image = image.resize(size, Image.LANCZOS)  # Resize ảnh về kích thước mong muốn

    # Tạo mặt nạ bo góc
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius, fill=255)

    # Áp dụng mặt nạ lên ảnh
    image.putalpha(mask)

    return ImageTk.PhotoImage(image)

def create_fav_button(parent, x, y, width, height, img_default, img_clicked, command=None):
    """
    Hàm tạo nút có hiệu ứng đổi ảnh khi nhấn.
    - parent: Frame hoặc Tk window chứa nút.
    - x, y, width, height: Tọa độ và kích thước nút.
    - img_default: Ảnh mặc định.
    - img_clicked: Ảnh khi nhấn.
    - command: Hàm sẽ gọi khi bấm vào nút (tùy chọn).
    """
    button_state = {"clicked": False}

    def toggle_image():
        button_state["clicked"] = not button_state["clicked"]
        button.config(image=img_clicked if button_state["clicked"] else img_default)
        if command:
            command()  # Gọi hàm nếu có

    button = tk.Button(
        parent,
        image=img_default,
        command=toggle_image,
        relief="flat"
    )
    button.place(x=x, y=y, width=width, height=height)

def create_toggle_button(parent, name, x, y, command, button_states, group):
    """
    Tạo button với hiệu ứng đổi ảnh khi click.
    - parent: Frame chứa button.
    - name: Tên button.
    - x, y: Tọa độ button.
    - command: Hàm xử lý khi bấm.
    - button_states: Dictionary lưu trạng thái các button.
    - group: Nhóm button ("mood", "sleeping_time", "event").
    """

    # Load ảnh cho button
    normal_image = PhotoImage(file=relative_to_assets(f"m_{name}_click.png"))  # Ảnh xám
    clicked_image = PhotoImage(file=relative_to_assets(f"m_{name}.png"))  # Ảnh màu

    def toggle_button():
        """Hàm xử lý khi click vào button."""
        if group in ["mood", "sleeping_time"]:  # Chỉ khóa nếu thuộc nhóm mood hoặc sleeping_time
            for btn_name, btn in button_states[group].items():
                if btn_name != name:
                    btn.config(image=btn.normal_image)  # Reset các nút khác về màu xám
                    btn.is_selected = False

        if not button.is_selected:
            button.config(image=clicked_image)
            button.is_selected = True
            command(name)  # Gọi hàm xử lý khi chọn
        else:
            button.config(image=normal_image)
            button.is_selected = False

    # Tạo button
    button = Button(parent, image=normal_image, bd=0, highlightthickness=0, borderwidth=0, command=toggle_button)
    button.normal_image = normal_image
    button.clicked_image = clicked_image
    button.is_selected = False
    button.place(x=x, y=y)

    # Thêm button vào nhóm quản lý
    if group not in button_states:
        button_states[group] = {}
    button_states[group][name] = button

    return button


# Hàm giới hạn ký tự bên frame 6
def limit_text_input(text_widget, label_widget, max_length=300):
    """
    Giới hạn số ký tự nhập vào Text Widget và cập nhật bộ đếm.

    - text_widget: Widget cần giới hạn.
    - label_widget: Nhãn hiển thị bộ đếm.
    - max_length: Số ký tự tối đa.
    """

    def on_text_change(event=None):
        text = text_widget.get("1.0", "end-1c")  # Lấy toàn bộ nội dung
        if len(text) > max_length:
            text_widget.delete("1.0", "end")  # Xóa toàn bộ nội dung
            text_widget.insert("1.0", text[:max_length])  # Chỉ giữ lại 300 ký tự

        # Cập nhật bộ đếm
        label_widget.config(text=f"{len(text_widget.get('1.0', 'end-1c'))}/{max_length}")

    text_widget.bind("<KeyRelease>", on_text_change)  # Cập nhật ngay khi nhập

class MarqueeText:
    def __init__(self, canvas, x1, y1, x2, y2, text, speed=10, font_size=27):
        self.canvas = canvas
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.speed = speed
        self.text = text

        # Tạo vùng chữ nhật màu đen
        self.clip_rect = canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="")

        # Tạo một canvas con để chứa chữ và giới hạn hiển thị
        self.text_canvas = tk.Canvas(canvas, bg="black", width=x2 - x1, height=y2 - y1, highlightthickness=0)
        self.text_canvas.place(x=x1, y=y1)

        # Tạo văn bản bên trong vùng này (chữ trắng)
        self.text_id = self.text_canvas.create_text(
            x2 - x1, (y2 - y1) // 2,
            text=text,
            anchor="w",
            font=("Crimson Pro SemiBold", font_size),
            fill="white"
        )

        # Lấy chiều rộng thực tế của văn bản
        self.text_width = self.text_canvas.bbox(self.text_id)[2] - self.text_canvas.bbox(self.text_id)[0]

        # Bắt đầu hiệu ứng chạy chữ
        self.animate()



    def animate(self):
        """Di chuyển chữ từ phải sang trái, khi hết chữ sẽ reset vị trí"""
        x, _, _, _ = self.text_canvas.bbox(self.text_id)

        # Nếu số ký tự nhỏ hơn hoặc bằng 20, giữ nguyên vị trí
        if len(self.text) <= 30:
            self.text_canvas.moveto(self.text_id, 0, 0)
        else:
            # Nếu chữ chạy hết ra khỏi vùng hiển thị thì reset vị trí
            if x + self.text_width < 0:
                self.text_canvas.moveto(self.text_id, self.x2 - self.x1, 0)
            else:
                self.text_canvas.move(self.text_id, -self.speed, 0)

        # Cập nhật lại sau mỗi 20ms
        self.text_canvas.after(30, self.animate)

    def set_text(self, new_text):
        """Cập nhật nội dung văn bản và khởi động lại hiệu ứng."""
        self.text = new_text
        self.text_canvas.itemconfig(self.text_id, text=self.text)  # Cập nhật văn bản

        # Cập nhật lại chiều rộng của văn bản sau khi thay đổi nội dung
        self.text_width = self.text_canvas.bbox(self.text_id)[2] - self.text_canvas.bbox(self.text_id)[0]

        # Đặt lại vị trí văn bản để bắt đầu chạy từ bên phải
        self.text_canvas.moveto(self.text_id, self.x2 - self.x1, 0)

def update_text_position(canvas, text_id, event):
    """Cập nhật vị trí text khi kích thước canvas thay đổi"""
    canvas.coords(text_id, event.width // 2, 65)  # Giữ chữ nằm giữa
def truncate_text(text, max_length=33):
    """Cắt chuỗi nếu dài hơn max_length, thêm '...' vào cuối."""
    if len(text) > max_length:
        return text[:30] + "..."
    return text
