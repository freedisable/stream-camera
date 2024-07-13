import socket
import cv2
import pickle
import struct
import random
# Tạo socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '127.0.0.1'  # Thay bằng IP của server
port = 9999
client_socket.connect((host_ip, port))

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K
        if not packet: break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)
    frame_flip = cv2.flip(frame,1)
    cv2.imshow("RECEIVING VIDEO 1", frame_flip)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()
