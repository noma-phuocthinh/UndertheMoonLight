from pathlib import Path
from tkinter import Toplevel, Canvas, Button, PhotoImage

# Định nghĩa đường dẫn đến thư mục chứa assets
base_dir=Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Qmess"/"asset_component"

def relative_to_assets(path: str) -> Path:
    """Hàm chuyển đổi đường dẫn ảnh"""
    return ASSETS_PATH / Path(path)

class Qmess_dntc:
    @staticmethod
    def show_window(parent=None, on_close=None):
        """Hiển thị cửa sổ thông báo đăng nhập thành công"""
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
            dn_Qmess_dntc_image = PhotoImage(file=relative_to_assets("Qmess_nho.png"))
            dn_Qmess_dntc_oker_image = PhotoImage(file=relative_to_assets("Qmess_oker.png"))
        except Exception:
            return

        # Hiển thị ảnh nền
        canvas.create_image(225.0, 106.0, image=dn_Qmess_dntc_image)

        # Hiển thị thông báo đăng nhập thành công
        canvas.create_text(
            225, 100,
            text="    Cậu đã đăng nhập\ntài khoản thành công",
            fill="#000000",
            font=("Crimson Pro SemiBold", 20),
            anchor="center"
        )

        def close_window():
            """Đóng cửa sổ và gọi hàm on_close nếu có"""
            window.destroy()  # Đóng cửa sổ
            if on_close:
                on_close()


        # Nút OK
        dn_Qmess_dntc_oker = Button(
            window,
            image=dn_Qmess_dntc_oker_image,
            borderwidth=0,
            highlightthickness=0,
            command=close_window,
            relief="flat"
        )
        dn_Qmess_dntc_oker.place(x=151.0, y=137.0, width=148.0, height=34.0)



        # Giữ tham chiếu hình ảnh
        window.dn_Qmess_dntc_image = dn_Qmess_dntc_image
        window.dn_Qmess_dntc_oker_image = dn_Qmess_dntc_oker_image

        # Khi người dùng bấm X để tắt cửa sổ
        window.protocol("WM_DELETE_WINDOW", close_window)
