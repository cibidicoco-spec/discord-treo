import os
import random
import string
import time
import requests


def generate_random_string(min_len=8, max_len=15):
    """Tạo chuỗi ký tự ngẫu nhiên gồm chữ cái và số"""
    length = random.randint(min_len, max_len)
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def main():
    # 1. Đọc các thông tin cấu hình từ Railway Environment Variables
    TOKEN = os.getenv("TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    # Đọc thời gian chờ (mặc định 5s nếu không nhập hoặc nhập sai)
    try:
        DELAY = float(os.getenv("DELAY", "5"))
    except ValueError:
        DELAY = 5.0

    # Lựa chọn spam ngẫu nhiên hay nội dung cố định
    # Nếu SPAM_RANDOM = "yes" hoặc "true" -> Spam ngẫu nhiên 8-15 ký tự
    # Nếu SPAM_RANDOM là bất kỳ nội dung nào khác -> Spam chính chữ đó!
    SPAM_RANDOM = os.getenv("SPAM_RANDOM", "yes").strip()

    if not TOKEN or not CHANNEL_ID:
        print(
            "❌ Lỗi: Chưa cấu hình TOKEN hoặc CHANNEL_ID trong Railway Variables!"
        )
        return

    url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
    headers = {"Authorization": TOKEN, "Content-Type": "application/json"}

    print("🚀 Bot đã sẵn sàng chạy trên Railway...")
    print(f"⏱️ Thời gian giãn cách giữa các tin nhắn: {DELAY} giây")

    if SPAM_RANDOM.lower() in ["yes", "y", "true"]:
        print("🔀 Chế độ: Spam KÝ TỰ NGẪU NHIÊN (8-15 ký tự)")
    else:
        print(f"📝 Chế độ: Spam CỐ ĐỊNH nội dung -> '{SPAM_RANDOM}'")

    print("-" * 40)

    while True:
        # Xác định nội dung tin nhắn gửi đi
        if SPAM_RANDOM.lower() in ["yes", "y", "true"]:
            content = generate_random_string(8, 15)
        else:
            content = SPAM_RANDOM

        payload = {"content": content}

        try:
            res = requests.post(url, headers=headers, json=payload)

            if res.status_code == 200:
                print(f"✅ Gửi thành công: {content}")
            elif res.status_code == 429:
                # Bị Discord giới hạn tần suất (Rate limited)
                retry_after = res.json().get("retry_after", 5)
                print(
                    f"⚠️ Bị giới hạn tần suất! Chờ {retry_after}s rồi gửi lại..."
                )
                time.sleep(retry_after)
            else:
                print(f"❌ Gửi thất bại! Code: {res.status_code} | {res.text}")

        except Exception as e:
            print(f"💥 Có lỗi kết nối: {e}")

        # Chờ theo khoảng thời gian đã đặt
        time.sleep(DELAY)


if __name__ == "__main__":
    main()
