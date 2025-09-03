from pathlib import Path
from tkinter import Toplevel, Canvas, Button, PhotoImage

# Định nghĩa đường dẫn đến thư mục chứa assets
base_dir=Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Qmess"/"asset_component"

def relative_to_assets(path: str) -> Path:
    """Hàm chuyển đổi đường dẫn ảnh"""
    return ASSETS_PATH / Path(path)

class Qmess_mk2sai:
    @staticmethod
    def show_window(parent=None):
        """Hiển thị cửa sổ thông báo mật khẩu nhập lại không khớp"""
        window = Toplevel(parent)

        window.after(10, lambda: window.deiconify())  # Hiển thị sau 10ms
        window_width = 450  # Độ rộng cửa sổ
        window_height = 213  # Độ cao cửa sổ
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window.configure(bg="#FFFFFF")
        window.resizable(False, False)

        canvas = Canvas(
            window,
            bg="#FFFFFF",
            height=213,
            width=450,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        try:
            dk_Qmess_mk2sai_image = PhotoImage(file=relative_to_assets("Qmess_nho.png"))
            dk_Qmess_mk2sai_thulai_image = PhotoImage(file=relative_to_assets("Qmess_thulai.png"))
        except Exception:
            return

        # Hiển thị ảnh nền
        canvas.create_image(225.0, 106.0, image=dk_Qmess_mk2sai_image)

        # Hiển thị thông báo lỗi
        canvas.create_text(
            225, 100,  # Căn giữa canvas
            text="Mật khẩu lần 2 không đúng",
            fill="#000000",
            font=("Crimson Pro SemiBold", 20),
            anchor="center"
        )

        def close_window():
            """Đóng cửa sổ khi bấm nút"""
            window.destroy()

        # Nút thử lại
        dk_Qmess_mk2sai_thulai = Button(
            window,
            image=dk_Qmess_mk2sai_thulai_image,
            borderwidth=0,
            highlightthickness=0,
            command=close_window,
            relief="flat"
        )
        dk_Qmess_mk2sai_thulai.place(x=151.0, y=137.0, width=148.0, height=34.0)

        # # Giữ tham chiếu hình ảnh
        # window.dk_Qmess_mk2sai_image = dk_Qmess_mk2sai_image
        # window.dk_Qmess_mk2sai_thulai_image = dk_Qmess_mk2sai_thulai_image

        window.mainloop()
