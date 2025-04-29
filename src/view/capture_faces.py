import cv2
import os

def capture_faces(person_name, save_dir="dataset", num_samples=100):
    person_path = os.path.join(save_dir, person_name)
    os.makedirs(person_path, exist_ok=True)
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    count = 0
    print(f"[*] Đang thu thập ảnh cho: {person_name}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face_img, (100, 100))
            img_path = os.path.join(person_path, f"{count+1}.jpg")
            cv2.imwrite(img_path, face_resized)
            count += 1
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"So anh :{count}/{num_samples}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Thu thập khuôn mặt", frame)
        if count >=100 or cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if count >= num_samples:
            break
    cap.release()
    cv2.destroyAllWindows()
    print(f"[✓] Đã lưu {count} ảnh vào: {person_path}")
    
if __name__ == "__main__":
    name = input("Nhập tên người cần thu thập ảnh: ")
    capture_faces(name)