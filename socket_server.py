import socket
import cv2
import pickle
import struct

# Tạo socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '0.0.0.0'
host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Bind socket
server_socket.bind(socket_address)

# Đặt chế độ lắng nghe
server_socket.listen(5)
print("LISTENING AT:", socket_address)

# Chấp nhận kết nối từ client
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)  # Thay đổi 0 bằng URL của camera IP nếu có
        while vid.isOpened():
            img, frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            try:
                client_socket.sendall(message)
            except:
                client_socket.close()
                print("client disconnected!")
                break
            # cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
        vid.release()
        cv2.destroyAllWindows()
