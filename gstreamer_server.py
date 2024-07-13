import cv2
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)

# Thiết lập pipeline GStreamer để truyền video qua RTSP
pipeline = (
    "appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! "
    "rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=0.0.0.0 port=8554"
)

# Khởi tạo video capture từ camera
cap = cv2.VideoCapture(0)  # Thay đổi 0 bằng URL của camera IP nếu có

# Thiết lập GStreamer pipeline
out = cv2.VideoWriter(pipeline, cv2.CAP_GSTREAMER, 0, 30, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
    cv2.imshow('Streaming', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
