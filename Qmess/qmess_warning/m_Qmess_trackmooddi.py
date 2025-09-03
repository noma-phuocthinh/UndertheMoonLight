from pathlib import Path
from tkinter import Toplevel, Canvas, Button, PhotoImage

base_dir=Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Qmess"/"asset_component"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Qmess_trackmooddi:
    @staticmethod
    def show_window(parent=None):
        """Hiển thị cửa sổ yêu cầu track mood"""
        window = Toplevel(parent)

        # Thiết lập kích thước cửa sổ
        window.after(10, lambda: window.deiconify())
        window_width = 450
        window_height = 213
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
            # Load hình ảnh
            m_Qmess_trackmooddi_image = PhotoImage(file=relative_to_assets("Qmess_nho.png"))
            m_Qmess_trackmooddi_thulai_image = PhotoImage(file=relative_to_assets("Qmess_thulai.png"))
        except Exception:
            return

        #tạo hình nền
        canvas.create_image(225.0, 106.0, image=m_Qmess_trackmooddi_image)

        #Hiển thị ảnh nền
        canvas.create_text(
            220,95,
            text="          Cậu chưa track mood\nvới sleeping time đúng hăm :)",
            fill="#000000",
            font=("Crimson Pro SemiBold", 20),
            anchor = "center"
        )

        def close_window():
            """Đóng cửa sổ khi bấm nút"""
            window.destroy()


        # Nút thử lại
        m_Qmess_trackmooddi_thulai = Button(
            window,
            image= m_Qmess_trackmooddi_thulai_image,
            borderwidth=0,
            highlightthickness=0,
            command=close_window,
            relief="flat"
        )
        m_Qmess_trackmooddi_thulai.place(x=151.0, y=137.0, width=148.0, height=34.0)

        window.mainloop()
