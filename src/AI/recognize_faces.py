import cv2
import os
import numpy as np

trainer_file = "trainer.yml"
dataset_path = "dataset"

face_recognizer = cv2.face.LBPHFaceRecognizer_create() #bộ nhận diện khuôn mặt sử dụng thuật toán LBPH
face_recognizer.read(trainer_file) #đọc dữ liệu từ file trainẻ

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #load mô hình Haar cascade nhận diện kmat tiếp

label_map = {i: name for i, name in enumerate(os.listdir(dataset_path))} #lấy danh sách thư mục trong dataset, mỗi thư mục tương ứng với một người và mỗi người 1 nhãn

cap = cv2.VideoCapture(0) #mở webcam

while True: #khúc này cũng giống khúc train
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces: #dự đoán khuôn mặt bằng nhãn
        face_img = gray[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face_img)

        if confidence < 100: #nhỏ hơn 100 thì gán label_map (tên) và độ chính xác
            name = label_map.get(label, "Unknown")
            confidence_text = f"{100 - confidence:.2f}%"
        else: #thằng này là người lạ
            name = "Unknown"
            confidence_text = ""

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #vẽ khugn
        cv2.putText(frame, f"{name} {confidence_text}", (x, y-10), #hiển thị tên
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('x'): #ấn x để dừng
        break

cap.release()
cv2.destroyAllWindows() #xoá hết
