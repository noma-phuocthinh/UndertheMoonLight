from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Scrollbar, Frame, Toplevel

# Định nghĩa đường dẫn đến thư mục chứa assets
base_dir=Path(__file__).parents[2]
ASSETS_PATH = base_dir/"Qmess"/"asset_component"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Qmess_tarot:
    @staticmethod
    def show_window(parent=None, on_close=None):
        """Hiển thị cửa sổ Qmess Tarot"""
        window = Toplevel(parent)
        window.after(10, lambda: window.deiconify())  # Hiển thị sau 10ms
        window_width = 1007  # Độ rộng cửa sổ
        window_height = 709  # Độ cao cửa sổ
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
            height=709,
            width=1007,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        try:
            Qmess_tr_backgr_image = PhotoImage(file=relative_to_assets("Qmess_tr_backgr.png"))
            Qmess_tr_thulai_image = PhotoImage(file=relative_to_assets("Qmess_tr_thulai.png"))
            window.Qmess_tr_backgr_image = Qmess_tr_backgr_image  # Giữ tham chiếu để tránh bị xóa bộ nhớ
            window.Qmess_tr_thulai_image = Qmess_tr_thulai_image  # Giữ tham chiếu ảnh
            canvas.create_image(503.0, 354.0, image=Qmess_tr_backgr_image)
        except Exception as e:
            return

        # Tạo frame chứa Text và Scrollbar
        text_frame = Frame(window, bg="#FFFFFF")
        text_frame.place(x=50, y=150, width=910, height=400)

        # Tạo Text widget
        text_widget = Text(
            text_frame,
            wrap="word",
            font=("Crimson Pro Light", 17),
            bg="#D9D9D9",
            fg="#000000",
            padx=10,
            pady=10
        )
        text_widget.insert("1.0", """Tarot là một bộ bài 78 lá được sử dụng từ thế kỷ 15 tại Ý và dần phát triển tiếng tăm ra toàn thế giới. 78 lá bài sẽ được chia ra 22 lá Ẩn chính (Major Arcana) và 56 lá Ẩn phụ (Minor Arcana), được đánh số La Mã. Bộ Ẩn phụ sẽ được chia tiếp theo 4 chất tương ứng với 4 nguyên tố Khí, Lửa, Nước, Đất. Mỗi chất này bao gồm 14 lá, gồm 10 lá được đánh số, và 4 lá Hoàng gia (Page, Knight, Queen, King - tựa như những lá hình của tú lơ khơ). Còn bộ Ẩn chính, tụi mình sẽ bàn thêm một chút ở đoạn sau. Sau khi nhận câu hỏi và trò chuyện, người đọc (Tarot reader) sẽ xào, rút, trải bài và bắt đầu đọc bài với mục đích chính là đưa ra phân tích, hướng dẫn, lời khuyên hoặc thậm chí là dự báo. 

Thoạt đầu nghe cũng giống như một trò chơi phải không? Kể cả vậy, từ thế kỷ 20, một số chuyên gia tâm lý đã bắt đầu quan tâm tới chủ nghĩa thần bí (mysticism) trong tâm lý học, khoa học nhận thức và cả vật lý hiện đại để những công cụ “thần bí” có phần dễ dàng tiếp cận hơn trong thời đại mới [1]. Ví dụ như Carl Jung cho rằng những lá bài Tarot là cách dễ dàng để thể hiện những nguyên mẫu của con người - và cả những đặc tính chung như sức mạnh nội tại, tham vọng, đam mê - được đề cập trong tâm lý học. Ông cũng nhận định chính điều này khiến Tarot trở thành công cụ lý tưởng cho quá trình trị liệu và theo dõi sức khoẻ tinh thần [2]. Cùng nhận định trên, Tarot còn được Carl Jung xem là một cây cầu phi lý trí giúp kết nối vùng vô thức và vùng ý thức [3]. Tới ngày nay, một số nhà hoạt động xã hội và nhà trị liệu tâm lý đều cởi mở với việc thân chủ tìm tới Tarot [4] như Charlynn Ruan, nhà tâm lý học lâm sàng và người sáng lập Thrive Psychology Group tại California, có đề cập trong bài phỏng vấn trên New York Times rằng cũng có khi, việc cùng thân chủ nghe lại buổi xem Tarot dẫn tới những kết quả “vượt cạn” bất ngờ và cho rằng: “Có rất nhiều chủ đề trong tâm lý học từng bị cho rằng quá khác biệt và “edgy” (tạm dịch: mang tính thách thức) [4].” 

Có được sự tán thành là thế, tại sao trong chúng ta vẫn thường lắc đầu, xua tay và có chút coi thường những người tin tưởng vào Tarot? Mình dám nghĩ rằng đó là vì mọi người nghi ngờ những thứ gọi là “trùng hợp ngẫu nhiên.” Đôi khi, chúng ta cần sự logic, lý trí, lý do cụ thể cho mọi điều để cảm thấy vững chãi, an toàn và không bị mông lung. Nếu mọi thứ tự-nhiên-mà-xảy-ra, thì lại dẫn tới cảm giác mất kiểm soát và lo lắng vì tương lai vô định. Có thể bạn cho rằng Tarot phù phiếm bởi nếu bạn muốn tin, bạn sẽ cho nó là đúng và nếu không thì ngược lại; hoặc bạn tin rằng cuộc đời mình là do mình quyết định, chính bởi vậy tạo ra những luồng suy nghĩ chỉ riêng bạn hiểu, và có sự lớp lang, sâu sắc hơn những lá bài với hình thù ngẫu nhiên, kỳ lạ (trong một số trường hợp còn là “dễ thương” nữa).

Nếu thực vậy, mình muốn nói rằng mình không hề phủ nhận rằng lập luận trên của bạn là sai. Đúng là cuộc đời bạn do bạn quyết định và những luồng suy nghĩ của riêng bạn sẽ không được đoán định bởi lá bài hay bất kỳ ai. Tuy vậy, cá nhân mình muốn chỉ ra thêm 2 điều: Thứ nhất, Tarot thực chất ủng hộ lập luận đó và thứ hai, ý nghĩa của những lá bài không hề có sự ngẫu nhiên.

Đặc biệt, 22 lá của bộ Ẩn chính trong Tarot tái hiện hành trình trải nghiệm cuộc sống từ khi sinh ra và theo đó là hành trình thấu hiểu bản thân. Bên cạnh đó, bạn có thể hiểu ý nghĩa mỗi lá qua mô hình cấu trúc nhân cách của Freud: Lá I-VII biểu trưng cho Bản năng (id), lá VIII-XIV là Bản ngã (ego) và XV-XXI là Siêu ngã (superego)[5]. 

The Fool (0) - lá đầu tiên của bộ bài Tarot không được đánh số - thể hiện sự khởi đầu và đại diện cho mỗi chúng ta khi bắt đầu cuộc hành trình đời mình.  Theo Shi Shuya, lá I-VII đại diện cho những tính chất nguyên thuỷ và cơ bản nhất. Theo học thuyết về các nguyên mẫu của Carl Jung, The Magician (I) và The High Priestess (II) đại diện cho sự đối lập của vạn vật: năng lượng hướng ngoại và khám phá nội tâm. Với 2 lá tiếp theo là The Empress (III) và The Emperor (IV) cũng là hai ý niệm tương quan và có thể áp vào nguyên mẫu của Carl Jung.   The Empress đại diện cho Tính nữ (Anima) và The Emperor là Tính nam (Animus) - và cũng thể hiện sự ảnh hưởng của hình ảnh một gia đình truyền thống nơi người cha và người mẹ có vai trò và tính chất rất rõ ràng.  The Empress truyền năng lượng sự nuôi dưỡng về tinh thần, thể chất, trong khi The Emperor toả ra khí chất đầy quyền lực và có kỷ luật. 

Và cứ thế, 21 lá Ẩn chính lần lượt kể lên hành trình của Chàng khờ - hay là The Fool - cũng chính là mỗi con người.

Mỗi lá bài mang theo hình ảnh của thế giới thực tại, của vũ trụ bao gồm cả yếu tố tôn giáo, văn hoá - xã hội, lịch sử... giúp bạn quan sát chính từng chặng, từng khoảnh khắc cuộc sống và nội tại của bản thân. Theo đó, người đọc bài sẽ dùng khả năng dẫn chuyện để kết nối các chi tiết, khơi mở và phân tích giúp người hỏi tự chiêm nghiệm ra lời hướng dẫn cho câu chuyện của riêng mình - đây là cách Tarot giúp bạn độc lập suy nghĩ và đưa ra quyết định cho cuộc đời của mình, chứ không phải để dự đoạn đích xác rằng bạn phải làm gì.
Cũng cần ghi nhớ một điều tất yếu: đó là Tarot không thể thay thế trị liệu tâm lý, đặc biệt là khi bạn có những vấn đề cần ý kiến và can thiệp của chuyên gia. Nhưng Tarot - cũng như việc viết nhật ký hành trình (journalling), hay chế độ “eat clean” hay việc tập thể dục - là một công cụ hỗ trợ tâm lý lành mạnh, phù hợp giúp bạn đào sâu bản thân, có góc nhìn bao dung và tổng quát hơn thay vì chỉ chăm chăm vào một chi tiết nhỏ như sự tức giận, tủi hổ hay thậm chí là sự tích cực - mà bạn có khi bị ám ảnh.

Mình xin được phép kết lại là ai cũng có thể tìm đến sự an ủi từ Tarot - dù bạn vô thần, đến từ đâu và có câu hỏi gì. Nếu dám đặt niềm tin, muốn tìm hiểu, bạn sẽ nhận ra Tarot không tạo hiệu ứng giả dược dù cũng là một cách “đánh lừa” trí óc - hay đúng hơn là “tôi luyện” cho bộ não chúng ta trở nên lành-mạnh hơn.  Cũng giống như một buổi trị liệu tâm lý, người đọc bài và chính những lá bài Tarot không mang mục đích đánh giá và áp đặt. Cũng giống như chọn người tham vấn tâm lý, mỗi Tarot reader sẽ có phong cách riêng, kèm theo đó là những quy tắc, công cụ, thế giới quan và tầm nhận thức khác nhau. Có chăng sự khác biệt lớn nhất chính là đặc tính dễ tiếp cận khiến Tarot chuyển hoá thành một “hiệu ứng”, một xu hướng mới lạ của giới trẻ thay vì được nhìn nhận như một công cụ hướng dẫn giúp ta hiểu mình hơn.

Lần tới khi thấy một video trải bài chung, hãy bấm vào và hít thở sâu, lắng nghe chính mình và chọn một tụ mà xem. Biết đâu bạn nhận ra sự an ủi lại đến từ chính việc dám cho bản thân thử một điều gì mới mẻ thì sao?""")

        text_widget.config(state="disabled")
        text_widget.pack(side="left", fill="both", expand=True)

        # Thêm thanh cuộn Scrollbar
        scrollbar = Scrollbar(text_frame, command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)

        def close_window():
            """Đóng cửa sổ khi bấm nút"""
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", close_window)

        # Nút bấm "Tiếp tục"
        Qmess_tr_thulai_image = Button(
            window,
            image=Qmess_tr_thulai_image,
            borderwidth=0,
            highlightthickness=0,
            command=close_window,
            relief="flat"
        )
        Qmess_tr_thulai_image.place(x=424.0, y=609.0, width=159.0, height=44.0)