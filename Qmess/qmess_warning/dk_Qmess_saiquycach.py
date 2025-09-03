from pathlib import Path
from tkinter import Toplevel, Canvas, Button, PhotoImage

# Định nghĩa đường dẫn assets
base_dir=Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Qmess"/"asset_component"

def relative_to_assets(path: str) -> Path:
    """Hàm chuyển đổi đường dẫn ảnh"""
    return ASSETS_PATH / Path(path)

class Qmess_saiquycach:
    @staticmethod
    def show_window(parent=None):
        """Hiển thị cửa sổ thông báo tên tài khoản không hợp lệ"""
        window = Toplevel(parent)

        window.after(10, lambda: window.deiconify())  # Hiển thị sau 10ms
        window_width = 450  # Độ rộng cửa sổ
        window_height = 270  # Độ cao cửa sổ
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
            height=270,
            width=450,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        try:
            dk_Qmess_saiquycach_image = PhotoImage(file=relative_to_assets("Qmess_lon.png"))
            dk_Qmess_saiquycach_thulai_image = PhotoImage(file=relative_to_assets("Qmess_thulai.png"))
        except Exception:
            return

        # Hiển thị ảnh nền
        canvas.create_image(225.0, 135.0, image=dk_Qmess_saiquycach_image)

        # Hiển thị thông báo lỗi
        canvas.create_text(
            225, 85,  # Căn giữa canvas
            text="Tên tài khoản không hợp lệ",
            fill="#000000",
            font=("Crimson Pro SemiBold", 22),
            anchor="center"
        )

        canvas.create_text(
            225, 140,  # Căn giữa và dịch xuống
            text="Tên tài khoản chỉ có thể chứa chữ cái, số, dấu gạch\nngang dưới (_), dấu chấm (.)",
            fill="#000000",
            font=("Crimson Pro Regular", 16),
            anchor="center"
        )

        def close_window():
            """Đóng cửa sổ khi bấm nút"""
            window.destroy()

        # Nút thử lại
        dk_Qmess_saiquycach_thulai = Button(
            window,
            image=dk_Qmess_saiquycach_thulai_image,
            borderwidth=0,
            highlightthickness=0,
            command=close_window,
            relief="flat"
        )
        dk_Qmess_saiquycach_thulai.place(x=138, y=195, width=159, height=44)

        window.mainloop()
