import cv2
import os

# Tạo thư mục lưu ảnh khuôn mặt nếu chưa có
dataset_path = "dataset"

cap = cv2.VideoCapture(0) # mở webcam
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #face_cascade:load mô hình Haar cascade để nhận diện khuôn mặt

name = input("Nhập tên của bạn: ")
user_folder = os.path.join(dataset_path, name)
if not os.path.exists(user_folder):
    os.makedirs(user_folder)

count = 0
print("Bắt đầu thu thập dữ liệu...")

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #chuyển sang màu xám dễ xiwr lý hơn
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #phát hiện khuôn mặt 

    for (x, y, w, h) in faces: #cắt khuôn mặt từ ảnh (face_img)
        count += 1
        face_img = frame[y:y+h, x:x+w]
        face_filename = os.path.join(user_folder, f"{count}.jpg") #lưu ảnh với tên 1.jpg, 2.jpg, ..., vào thư mục người dùng
        cv2.imwrite(face_filename, face_img)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #vẽ hình chữ nhật xung quanh khuôn mặt

    cv2.imshow('Capture Faces', frame) #hiển thị webcam với cái khung đã vẽ ở trên

    if cv2.waitKey(1) & 0xFF == count >= 30: #khi chụp đủ 30 ảnh sẽ dừng lại
        break

cap.release() #đóng webcam 
cv2.destroyAllWindows() #đóng cửa sổ hiển thị
print("Đã lưu ảnh khuôn mặt!")
