import os
import json


# Đọc tệp JSON
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Kiểm tra xem tệp có tồn tại không
def check_file_exists(file_path):
    return os.path.isfile(file_path)


# Kiểm tra các đường dẫn trong tệp JSON
def check_files_in_json(json_file_path):
    data = read_json(json_file_path)

    # Duyệt qua các trạng thái cảm xúc (angry, depressed, happy, normal, sad)
    for mood in data:
        print(f"Kiểm tra danh sách bài hát trạng thái cảm xúc: {mood}")

        for item in data[mood]:
            music_path = os.path.join('D:\\KTLT_PJ\\Data\\Music\\DATA_MUSIC', item.get('Music Path', ''))
            music_image = os.path.join('D:\\KTLT_PJ\\Data\\Music\\DATA_IMAGE', item.get('Music Image', ''))

            # Kiểm tra sự tồn tại của các tệp MP3 và PNG
            music_exists = check_file_exists(music_path)
            image_exists = check_file_exists(music_image)

            if music_exists:
                pass
            else:
                print(f"    - File MP3 {music_path} không tồn tại.")

            if image_exists:
                pass
            else:
                print(f"    - File PNG {music_image} không tồn tại.")


# Đường dẫn tệp JSON của bạn
json_file_path =r'D:\\KTLT_PJ\\Data\\Music\\data_music_sorted.json'
check_files_in_json(json_file_path)
