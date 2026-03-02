import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av

st.title("🔥 Ứng dụng Cảnh báo Đám cháy (Đã tối ưu hóa)")
st.write("Đã áp dụng kỹ thuật thu nhỏ ảnh để giảm giật lag.")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    # --- BẮT ĐẦU TỐI ƯU HÓA ---
    # 1. Thu nhỏ kích thước ảnh xuống một nửa (fx=0.5, fy=0.5) để xử lý nhanh hơn
    small_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

    # 2. Xử lý trên ảnh nhỏ: Làm mờ và chuyển màu
    blur = cv2.GaussianBlur(small_img, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # 3. Dải màu ngọn lửa
    lower_fire = np.array([10, 100, 100], dtype="uint8")
    upper_fire = np.array([30, 255, 255], dtype="uint8")

    # 4. Lọc ảnh
    mask = cv2.inRange(hsv, lower_fire, upper_fire)

    # 5. Đếm số lượng điểm ảnh. 
    # LƯU Ý: Vì ảnh đã nhỏ đi 4 lần (giảm một nửa chiều dài, một nửa chiều rộng), 
    # nên ta cũng phải giảm ngưỡng cảnh báo xuống tương ứng.
    fire_pixels = cv2.countNonZero(mask)

    # 6. Cảnh báo (Ngưỡng cũ là 1500, giờ giảm xuống khoảng 400)
    if fire_pixels > 400:
        # Chúng ta vẽ chữ lên 'img' (ảnh gốc to và rõ) chứ không vẽ lên 'small_img'
        cv2.putText(img, "CANH BAO: PHAT HIEN DAM CHAY!", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    # --- KẾT THÚC TỐI ƯU HÓA ---

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# Thêm tham số media_stream_constraints để yêu cầu camera chỉ gửi video ở độ phân giải vừa phải (640x480), tắt âm thanh (audio: False)
webrtc_streamer(
    key="fire-detection", 
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": {"width": 640, "height": 480}, "audio": False}
)
