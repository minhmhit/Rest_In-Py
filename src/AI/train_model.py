import cv2
import os
import numpy as np
from PIL import Image #đọc ảnh và chuyển đổi sang ảnh xám

dataset_path = "dataset"
trainer_file = "trainer.yml"

face_recognizer = cv2.face.LBPHFaceRecognizer_create() #nhận diện bằng LBPH tiếp
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') #bộ phát hiện khuôn mặt Haar cascade.

faces, labels = [], []

def get_images_and_labels(dataset_path): #hàm lấy ảnh và nhan
    label_id = 0
    label_map = {}
    for name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, name)
        if not os.path.isdir(person_path): 
            continue
        label_map[label_id] = name # cho mỗi người 1 id nhãn
        for image_name in os.listdir(person_path):
            img_path = os.path.join(person_path, image_name)
            img = Image.open(img_path).convert('L')
            img_numpy = np.array(img, 'uint8') #chueyẻn qua màu xám 
            
            faces.append(img_numpy) #thêm 2 cái này zo list
            labels.append(label_id)
        label_id += 1
    return label_map

label_map = get_images_and_labels(dataset_path) #gọi hàm
face_recognizer.train(faces, np.array(labels)) #train
face_recognizer.write(trainer_file) #ghi zo file

print("Training hoàn tất!")
print("Lưu mô hình vào:", trainer_file)
print("Label mapping:", label_map)
