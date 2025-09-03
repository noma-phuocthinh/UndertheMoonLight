from pathlib import Path
from tkinter import Toplevel, Canvas, Button, PhotoImage

# Định nghĩa đường dẫn đến thư mục chứa assets
base_dir=Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Qmess"/"asset_component"

def relative_to_assets(path: str) -> Path:
    """Hàm chuyển đổi đường dẫn ảnh"""
    return ASSETS_PATH / Path(path)

class Qmess_nhatkydi:
    @staticmethod
    def show_window(parent=None, controller=None):  # Thêm controller
        """Hiển thị cửa sổ thông báo track mood"""
        window = Toplevel(parent)
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
            m_Qmess_trackmooddi_image = PhotoImage(file=relative_to_assets("Qmess_nho2nut.png"))
            m_Qmess_trackmooddi_trangchu_image = PhotoImage(file=relative_to_assets("Qmess_trangchu.png"))
            m_Qmess_trackmooddi_oker_image = PhotoImage(file=relative_to_assets("Qmess_oker.png"))
        except Exception:
            return

        # Hiển thị ảnh nền
        canvas.create_image(225.0, 106.0, image=m_Qmess_trackmooddi_image)

        # Hiển thị thông báo
        canvas.create_text(
            72.0,
            55.0,
            anchor="nw",
            text="Bạn viết nhật đi rồi\nrồi nghe nhạc cùng tui ^^",
            fill="#000000",
            justify="center",
            font=("Crimson Pro SemiBold", 28 * -1)
        )

        # Nút Trang chủ
        m_Qmess_trackmooddi_trangchu = Button(
            window,
            image=m_Qmess_trackmooddi_trangchu_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (controller.show_frame("Frame04"), window.destroy()) if controller else print("Chưa có controller"),
            relief="flat"
        )
        m_Qmess_trackmooddi_trangchu.place(x=57.0, y=136.0, width=143.0, height=36.0)

        # Nút Thử lại
        m_Qmess_trackmooddi_thulai = Button(
            window,
            image=m_Qmess_trackmooddi_oker_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (controller.show_frame("Frame06"), window.destroy()) if controller else print("Chưa có controller"),
            relief="flat"
        )
        m_Qmess_trackmooddi_thulai.place(x=243.0, y=136.0, width=143.0, height=36.0)

        window.mainloop()
