import tkinter as tk
from Function.app_controller import AppController
from Frame.frame_01.frame_1 import Frame01
from Frame.frame_02.frame_2 import Frame02
from Frame.frame_03.frame_3 import Frame03
from Frame.frame_04.frame_4 import Frame04
from Frame.frame_05.frame_5 import Frame05
from Frame.frame_06.frame_6 import Frame06
from Frame.frame_07.frame_7 import Frame07
from Frame.frame_09.frame_9 import Frame09
from Frame.frame_10.frame_10 import Frame10
from Frame.frame_11.frame_11 import Frame11
from Frame.frame_12.frame_12 import Frame12
from Frame.frame_13.frame_13 import Frame13

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.controller = AppController(self)

        # Cấu hình cửa sổ chính
        self.geometry("1440x1024")
        self.title("Under the Moonlight")
        self.resizable(False, False)

        # Định vị cửa sổ giữa màn hình
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1440) // 2
        y = (screen_height - 1024) // 2
        self.geometry(f"1440x1024+{x}+{y}")

        # Tạo container chứa tất cả các frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Khởi tạo và lưu trữ tất cả các frame
        self.frames = {}
        for F in (
        Frame01, Frame02, Frame03, Frame04, Frame05,Frame06, Frame09,Frame10,Frame11,Frame07,Frame12,Frame13):
            frame = F(parent=container, controller=self.controller)
            self.frames[F.__name__] = frame
            self.controller.register_frame(F.__name__, frame)
            frame.grid(row=0, column=0, sticky="nsew")

        # Hiển thị Frame01 làm trang chủ
        self.controller.show_frame("Frame01")
if __name__ == "__main__":
    app = Main()
    app.mainloop()