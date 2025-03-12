import cv2  # Thư viện xử lý hình ảnh và video
import os   # Thư viện tương tác với hệ thống tệp
import time # Thư viện xử lý thời gian

# Tạo thư mục dataset nếu chưa tồn tại
dataset_path = "dataset"  # Đường dẫn đến thư mục chứa dữ liệu
if not os.path.exists(dataset_path):  # Kiểm tra xem thư mục đã tồn tại chưa
    os.makedirs(dataset_path)  # Nếu chưa tồn tại thì tạo mới

# Khởi tạo webcam
cap = cv2.VideoCapture(0)  # Mở webcam (0 là webcam mặc định)
if not cap.isOpened():  # Kiểm tra xem webcam có được mở thành công không
    print("Lỗi: Không thể mở webcam!")
    exit()

# Nạp mô hình nhận diện khuôn mặt Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
if face_cascade.empty():  # Kiểm tra xem mô hình có được nạp thành công không
    print("Lỗi: Không thể nạp file Haar Cascade!")
    exit()

# Nhập tên người dùng và tạo thư mục tương ứng
name = input("Nhập tên của bạn: ")  # Yêu cầu người dùng nhập tên
user_folder = os.path.join(dataset_path, name)  # Tạo đường dẫn đến thư mục người dùng
if not os.path.exists(user_folder):  # Kiểm tra xem thư mục đã tồn tại chưa
    os.makedirs(user_folder)  # Nếu chưa tồn tại thì tạo mới

# Hàm chụp ảnh theo góc
def capture_angle(angle_name, start_count=0, num_images=10):
    """
    Hàm chụp ảnh khuôn mặt theo góc nhất định
    
    Tham số:
        angle_name (str): Tên góc chụp ('front', 'left', 'right')
        start_count (int): Số thứ tự bắt đầu của ảnh
        num_images (int): Số lượng ảnh cần chụp
    
    Trả về:
        int: Tổng số ảnh đã chụp
    """
    count = start_count  # Bắt đầu đếm từ start_count
    target_count = start_count + num_images  # Số lượng ảnh cần đạt được
    
    # Chọn thông báo dựa trên góc chụp
    if angle_name == "front":
        message = "Vui long nhin thang vao camera"
    elif angle_name == "left":
        message = "Vui long quay mat qua ben trai"
    elif angle_name == "right":
        message = "Vui long quay mat qua ben phai"
    else:
        message = "Vui long dieu chinh goc chup"
    
    print(f"Bắt đầu chụp góc {angle_name}...")
    
    # Vòng lặp chụp ảnh
    while count < target_count:
        # Đọc frame từ webcam
        ret, frame = cap.read()  # ret: trạng thái đọc, frame: hình ảnh
        if not ret:  # Nếu không đọc được frame
            print("Lỗi: Không thể đọc frame từ webcam!")
            break
            
        # Chuyển đổi sang ảnh xám để tăng tốc độ xử lý
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Nhận diện khuôn mặt
        # Tham số: ảnh xám, tỷ lệ thu nhỏ (1.3), số lần lặp tối thiểu (5)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Hiển thị hướng dẫn trên frame
        cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Anh: {count+1-start_count}/{num_images}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Xử lý khuôn mặt nếu phát hiện được
        if len(faces) > 0:
            # Lấy khuôn mặt đầu tiên nếu phát hiện nhiều khuôn mặt
            x, y, w, h = faces[0]
            
            # Vẽ hình chữ nhật xung quanh khuôn mặt
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Chờ 0.5 giây trước khi chụp để tránh chụp nhiều ảnh cùng lúc
            # Cần show frame và kiểm tra key trước khi sleep
            cv2.imshow('Capture Faces', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):  # Nếu nhấn 'q' thì thoát
                return count
            
            time.sleep(0.5)  # Chờ 0.5 giây
            
            # Đọc frame mới sau khi đã chờ 0.5 giây
            ret, frame = cap.read()
            if not ret:
                print("Lỗi: Không thể đọc frame từ webcam!")
                break
                
            # Nhận diện khuôn mặt lại trên frame mới
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:  # Nếu vẫn phát hiện được khuôn mặt
                x, y, w, h = faces[0]
                
                # Cắt ảnh khuôn mặt
                face_img = frame[y:y+h, x:x+w]
                
                # Tăng biến đếm và lưu ảnh
                count += 1
                face_filename = os.path.join(user_folder, f"{count}.jpg")
                cv2.imwrite(face_filename, face_img)
                
                # Vẽ lại hình chữ nhật và hiển thị thông báo đã chụp
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Chup!", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Cập nhật hiển thị số ảnh đã chụp
                cv2.putText(frame, f"Anh: {count+1-start_count}/{num_images}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Hiển thị frame
        cv2.imshow('Capture Faces', frame)
        
        # Kiểm tra phím nhấn
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Nếu nhấn 'q' thì thoát
            break
    
    return count

# Danh sách các góc cần chụp
angles = ["front", "left", "right"]
image_count = 0

# Chụp ảnh cho từng góc
for angle in angles:
    prev_count = image_count  # Lưu số lượng ảnh trước khi chụp góc mới
    
    # Chụp ảnh cho góc hiện tại
    image_count = capture_angle(angle, start_count=image_count, num_images=10)
    
    # Hiển thị thông báo số ảnh đã chụp
    print(f"Đã chụp {image_count - prev_count} ảnh ở góc {angle}")
    
    # Chờ người dùng chuẩn bị cho góc tiếp theo (trừ góc cuối cùng)
    if angle != angles[-1]:
        print(f"Chuẩn bị chụp góc tiếp theo. Nhấn phím bất kỳ để tiếp tục...")
        cv2.waitKey(0)  # Chờ cho đến khi người dùng nhấn phím

# Giải phóng tài nguyên
cap.release()  # Giải phóng webcam
cv2.destroyAllWindows()  # Đóng tất cả cửa sổ
print(f"Hoàn thành! Đã lưu tổng cộng {image_count} ảnh khuôn mặt!")