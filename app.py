import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av

# Cấu hình giao diện trang web
st.title("🔥 Ứng dụng Cảnh báo Đám cháy qua Webcam")
st.write("Bật camera, cấp quyền truy cập và đưa một nguồn màu cam/vàng (như ngọn lửa từ bật lửa hoặc hình ảnh ngọn lửa trên điện thoại) vào camera để thử nghiệm.")

# Hàm này sẽ được gọi liên tục cho mỗi khung hình (frame) từ camera của bạn
def video_frame_callback(frame):
    # Chuyển đổi khung hình nhận được thành mảng dữ liệu ảnh để OpenCV có thể đọc
    img = frame.to_ndarray(format="bgr24")

    # 1. Làm mờ ảnh một chút để giảm nhiễu (giúp nhận diện màu tốt hơn)
    blur = cv2.GaussianBlur(img, (21, 21), 0)
    
    # 2. Chuyển đổi ảnh sang hệ màu HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # 3. Định nghĩa dải màu của ngọn lửa (Màu vàng/cam)
    # Bạn có thể điều chỉnh các con số này sau nếu nhận diện chưa chuẩn
    lower_fire = np.array([10, 100, 100], dtype="uint8")
    upper_fire = np.array([30, 255, 255], dtype="uint8")

    # 4. Lọc ảnh: Tạo ra một "mặt nạ" chỉ giữ lại những điểm ảnh nằm trong dải màu lửa
    mask = cv2.inRange(hsv, lower_fire, upper_fire)

    # 5. Đếm số lượng điểm ảnh (pixel) giống màu lửa
    fire_pixels = cv2.countNonZero(mask)

    # 6. Đưa ra cảnh báo nếu số pixel lửa vượt qua ngưỡng (ví dụ: 1500 pixel)
    if fire_pixels > 1500:
        # Vẽ dòng chữ màu đỏ lên khung hình
        cv2.putText(img, "CANH BAO: PHAT HIEN DAM CHAY!", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Trả lại khung hình đã được xử lý (có hoặc không có chữ cảnh báo) lên màn hình web
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Khởi chạy luồng camera và áp dụng hàm xử lý ảnh ở trên
webrtc_streamer(key="fire-detection", video_frame_callback=video_frame_callback)
