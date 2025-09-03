from pathlib import Path
from tkinter import Toplevel, Canvas, Button, PhotoImage

# Định nghĩa đường dẫn đến thư mục chứa assets
base_dir=Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Qmess"/"asset_component"

def relative_to_assets(path: str) -> Path:
    """Hàm chuyển đổi đường dẫn ảnh"""
    return ASSETS_PATH / Path(path)

class Qmess_tdtt_thanhcong:
    @staticmethod
    def show_window(parent=None, on_close=None):  # Thêm on_close vào tham số
        """Hiển thị cửa sổ thông báo đăng ký tài khoản thành công"""
        window = Toplevel(parent)
        #window.geometry("450x213")
        #window.configure(bg="#FFFFFF")
        #window.resizable(False, False)

        window.after(10, lambda: window.deiconify())  # Hiển thị sau 10ms #giảm nháy giảm nháy
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
            Qmess_tdtt_thanhcong_image = PhotoImage(file=relative_to_assets("Qmess_nho.png"))
            Qmess_tdtt_thanhcong_oker_image = PhotoImage(file=relative_to_assets("Qmess_oker.png"))
        except Exception as e:
            print(f"Lỗi khi tải ảnh: {e}")
            return

        # Hiển thị ảnh nền
        canvas.create_image(225.0, 106.0, image=Qmess_tdtt_thanhcong_image)

        # Hiển thị thông báo đăng ký thành công
        canvas.create_text(
            225, 100,
            text="      Cậu đã thay đổi\nthông tin thành công",
            fill="#000000",
            font=("Crimson Pro SemiBold", 20),
            anchor="center"
        )

        def close_window():
            """Đóng cửa sổ khi bấm nút"""
            window.destroy()

        # Nút OK
        Qmess_tdtt_thanhcong_oker = Button(
            window,
            image=Qmess_tdtt_thanhcong_oker_image,
            borderwidth=0,
            highlightthickness=0,
            command=close_window,  # Đóng cửa sổ khi bấm nút
            relief="flat"
        )
        Qmess_tdtt_thanhcong_oker.place(x=151.0, y=137.0, width=148.0, height=34.0)

        window.mainloop()
