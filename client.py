import cv2

url = 'http://127.0.0.1:5000/video_feed'

cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    flipped_frame = cv2.flip(frame, 1)
    cv2.imshow('Video Stream', flipped_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
