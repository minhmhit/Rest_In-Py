import cv2  # Thư viện xử lý hình ảnh và video
import os   # Thư viện tương tác với hệ thống tệp
import numpy as np  # Thư viện xử lý dữ liệu số

# Đường dẫn đến file đã train và thư mục dataset
trainer_file = "trainer.yml"  # File chứa dữ liệu huấn luyện
dataset_path = "dataset"  # Thư mục chứa dữ liệu khuôn mặt

# Kiểm tra xem file trainer có tồn tại không
if not os.path.exists(trainer_file):
    print(f"Lỗi: Không tìm thấy file {trainer_file}!")
    print("Hãy chạy chương trình huấn luyện trước.")
    exit()

# Kiểm tra xem thư mục dataset có tồn tại không
if not os.path.exists(dataset_path):
    print(f"Lỗi: Không tìm thấy thư mục {dataset_path}!")
    exit()

# Tạo bộ nhận diện khuôn mặt sử dụng thuật toán LBPH
# (Local Binary Patterns Histograms)
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(trainer_file)  # Đọc dữ liệu từ file trainer

# Nạp mô hình Haar cascade để nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
if face_cascade.empty():  # Kiểm tra xem mô hình có được nạp thành công không
    print("Lỗi: Không thể nạp file Haar Cascade!")
    exit()

# Tạo mapping từ nhãn (số) sang tên người
# Mỗi thư mục trong dataset là một người và sẽ được gán một nhãn
label_map = {i: name for i, name in enumerate(os.listdir(dataset_path))}
print("Danh sách người đã đăng ký:", list(label_map.values()))

# Thiết lập webcam
cap = cv2.VideoCapture(0)  # Mở webcam (0 là webcam mặc định)
if not cap.isOpened():  # Kiểm tra xem webcam có được mở thành công không
    print("Lỗi: Không thể mở webcam!")
    exit()

# Thiết lập ngưỡng tin cậy (càng thấp càng chính xác)
confidence_threshold = 70  # Ngưỡng tin cậy để xác định người lạ

# Biến đếm số khung hình
frame_count = 0

# Bắt đầu vòng lặp chính để nhận diện khuôn mặt
while True:
    # Đọc frame từ webcam
    ret, frame = cap.read()  # ret: trạng thái đọc, frame: hình ảnh
    if not ret:  # Nếu không đọc được frame
        print("Lỗi: Không thể đọc frame từ webcam!")
        break
    
    # Đếm số khung hình (để giảm tải CPU)
    frame_count += 1
    
    # Chuyển đổi sang ảnh xám để tăng tốc độ xử lý
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Nhận diện khuôn mặt trong frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Hiển thị thông tin hướng dẫn
    cv2.putText(frame, "Nhan 'x' de thoat", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Xử lý từng khuôn mặt được phát hiện
    for (x, y, w, h) in faces:
        # Cắt phần khuôn mặt từ ảnh xám
        face_img = gray[y:y+h, x:x+w]
        
        # Chuẩn hóa kích thước ảnh nếu cần
        try:
            # Nhận diện khuôn mặt và trả về nhãn và độ tin cậy
            label, confidence = face_recognizer.predict(face_img)
            
            # Xác định tên người dựa trên nhãn và độ tin cậy
            if confidence < confidence_threshold:  # Nếu độ tin cậy đủ cao
                name = label_map.get(label, "Unknown")  # Lấy tên từ label_map
                confidence_text = f"{100 - confidence:.1f}%"  # Chuyển đổi độ tin cậy thành phần trăm
                color = (0, 255, 0)  # Màu xanh lá cho người đã biết
            else:  # Nếu độ tin cậy thấp, xem như người lạ
                name = "Unknown"
                confidence_text = f"(Nguoi la)"
                color = (0, 0, 255)  # Màu đỏ cho người lạ
            
            # Vẽ hình chữ nhật xung quanh khuôn mặt
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Hiển thị tên và độ tin cậy
            cv2.putText(frame, f"{name}", (x, y-35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, f"{confidence_text}", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        except Exception as e:
            # Xử lý ngoại lệ khi không thể nhận diện khuôn mặt
            print(f"Lỗi khi nhận diện khuôn mặt: {e}")
            continue
    
    # Hiển thị số người trong frame và số người đã đăng ký
    cv2.putText(frame, f"So nguoi phat hien: {len(faces)}", (10, frame.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # Hiển thị frame
    cv2.imshow('Face Recognition', frame)
    
    # Kiểm tra phím nhấn
    if cv2.waitKey(1) & 0xFF == ord('x'):  # Nếu nhấn 'x' thì thoát
        break

# Giải phóng tài nguyên
cap.release()  # Giải phóng webcam
cv2.destroyAllWindows()  # Đóng tất cả cửa sổ
print("Chương trình đã kết thúc.")