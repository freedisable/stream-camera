from flask import Flask, Response
import cv2

app = Flask(__name__)
host = '0.0.0.0'
port = 5000
camera_url = f'http://{host}:{str(port)}/video_feed'
cap = cv2.VideoCapture(camera_url)

# Check if the connection to the camera URL was successful
if not cap.isOpened():
    # If not, fall back to the laptop camera
    cap = cv2.VideoCapture(0)

# Hàm để lấy dữ liệu từ camera và gửi đến client
def generate_frames():
    # cap = cv2.VideoCapture(0)  # Thay đổi 0 bằng URL của camera IP nếu có
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host, port)
