from flask import Flask, Response
import cv2
import subprocess
import numpy as np

# sudo apt update
# sudo apt install ffmpeg
# ffmpeg -version

app = Flask(__name__)

udp_stream_url = 'udp://<ip-server>:<port>'
ffmpeg_process = subprocess.Popen(
    ['ffmpeg', '-i', udp_stream_url, '-f', 'image2pipe', '-pix_fmt', 'bgr24', '-vcodec', 'rawvideo', '-'],
    stdout=subprocess.PIPE
)

# Function to get frames from the ffmpeg output and send to the client
def generate_frames():
    while True:
        raw_frame = ffmpeg_process.stdout.read(640 * 480 * 3)  # Adjust frame size as needed
        if len(raw_frame) != (640 * 480 * 3):
            break

        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((480, 640, 3))
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
