
from pathlib import Path
from tkinter import Toplevel, Canvas, Button, PhotoImage

# Định nghĩa đường dẫn đến thư mục chứa assets
base_dir=Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Qmess"/"asset_component"

def relative_to_assets(path: str) -> Path:
    """Hàm chuyển đổi đường dẫn ảnh"""
    return ASSETS_PATH / Path(path)

class Qmess_nhapsaiqc_kb:
    @staticmethod
    def show_window(parent=None):
        """Hiển thị cửa sổ thông báo nhập sai quy cách"""
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
            kb_Qmess_nhapsaiqc_image = PhotoImage(file=relative_to_assets("Qmess_lon.png"))
            kb_Qmess_nhapsaiqc_thulai = PhotoImage(file=relative_to_assets("Qmess_thulai.png"))
        except Exception:
            return

        # Hiển thị ảnh nền
        canvas.create_image(225.0, 135.0, image=kb_Qmess_nhapsaiqc_image)

        # Hiển thị thông báo
        canvas.create_text(
            38.0,
            86.0,
            anchor="nw",
            justify="center",
            text="Cậu nhập không đúng quy cách",
            fill="#000000",
            font=("Crimson Pro SemiBold", 28 * -1)
        )

        canvas.create_text(
            64.0,
            131.0,
            anchor="nw",
            text="Vui lòng nhập với cú pháp \u201cDD/MM/YYYY\u201d",
            justify="center",
            fill="#000000",
            font=("Crimson Pro Regular", 18 * -1)
        )

        def close_window():
            """Đóng cửa sổ khi bấm nút"""
            window.destroy()

        # Nút Thử lại
        close_button = Button(
            window,
            image=kb_Qmess_nhapsaiqc_thulai,
            borderwidth=0,
            highlightthickness=0,
            command=close_window,
            relief="flat"
        )
        close_button.place(x=139.0, y=196.0, width=159.0, height=44.0)

        window.mainloop()
