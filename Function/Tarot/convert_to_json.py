import json
import os
import re
from pathlib import Path

import pandas as pd

base_dir = Path(__file__).parents[2]
# Đường dẫn file Excel chứa thông tin lá bài
EXCEL_FILE = base_dir / "Function" / "Tarot" / "Book1.xlsx"

# Đường dẫn thư mục chứa hình ảnh
IMAGE_FOLDER = base_dir / "Data" / "Tarot" / "data_tarot_image"  # Đã sửa đây

# Tên file JSON xuất ra
JSON_FILE = base_dir / "Data" / "Tarot" / "tarot_cards.json"

# Đọc dữ liệu từ file Excel (giả sử thông tin ở sheet đầu tiên)
df = pd.read_excel(EXCEL_FILE)

# Danh sách tất cả file ảnh trong thư mục
image_files = os.listdir(IMAGE_FOLDER)

# Hàm chuẩn hóa tên để tìm kiếm chính xác hơn
def normalize_name(name):
    name = name.lower().strip()
    name = name.replace(" ", "_").replace("-", "_")  # Chuyển khoảng trắng và gạch ngang thành gạch dưới
    name = re.sub(r"[^a-z0-9_]", "", name)  # Loại bỏ ký tự đặc biệt
    return name

# Chuyển đổi dữ liệu từ DataFrame sang danh sách JSON
tarot_cards = []

for _, row in df.iterrows():
    card_name = str(row["TÊN LÁ BÀI"]).strip()  # Lấy tên lá bài
    keywords = str(row["TỪ KHÓA (01 TỪ)"]).strip()  # Lấy từ khóa
    meaning = str(row["Ý nghĩa Xuôi"]).strip()  # Lấy ý nghĩa xuôi

    # Tìm ảnh phù hợp trong thư mục
    image_path = ""
    normalized_card_name = normalize_name(card_name)

    for filename in image_files:
        normalized_filename = normalize_name(filename)
        if normalized_card_name in normalized_filename:  # Kiểm tra nếu tên lá bài xuất hiện trong tên file
            full_image_path = os.path.join(IMAGE_FOLDER, filename)  # Lưu đường dẫn đầy đủ
            if os.path.exists(full_image_path):  # Kiểm tra file có tồn tại không
                image_path = full_image_path
                break

    if not image_path:
        pass

    # Thêm vào danh sách
    tarot_cards.append({
        "Tên lá bài": card_name,
        "Từ khóa": keywords,
        "Ý nghĩa xuôi": meaning,
        "Hình ảnh": image_path.replace("\\", "/")  # Lưu đường dẫn đầy đủ
    })

# Lưu danh sách vào file JSON
with open(JSON_FILE, "w", encoding="utf-8") as file:
    json.dump(tarot_cards, file, indent=4, ensure_ascii=False)

