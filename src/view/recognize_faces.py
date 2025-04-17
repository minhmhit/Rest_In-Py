import numpy as np
import cv2
from PIL import Image
import os

IMAGE_SIZE = (100, 100)

def load_model(num_components=10):
    mean_face = np.load("mean_face.npy")
    eigvecs = np.load("eigvecs.npy")
    X_projected = np.load("X_projected.npy")
    labels = np.load("labels.npy")
    X_projected = X_projected[:num_components, :]
    eigvecs = eigvecs[:, :num_components]
    return mean_face, eigvecs, X_projected, labels

def preprocess_face_from_frame(gray_frame, face_coords):
    x, y, w, h = face_coords
    face_img = gray_frame[y:y+h, x:x+w]
    face_resized = cv2.resize(face_img, IMAGE_SIZE)
    face_flat = face_resized.flatten().reshape(-1, 1)
    return face_flat

def project_face(face, mean_face, eigvecs, num_components=10):
    face_diff = face - mean_face
    projection = np.dot(eigvecs[:, :num_components].T, face_diff)
    return projection

def recognize_face_from_projection(face_proj, X_projected, labels, label_map, threshold=1500):
    distances = np.linalg.norm(X_projected.T - face_proj.T, axis=1)
    best_match_idx = np.argmin(distances)
    min_distance = distances[best_match_idx]
    if min_distance > threshold:
        return "Unknown", min_distance
    predicted_label = labels[best_match_idx]
    for name, label in label_map.items():
        if label == predicted_label:
            return name, min_distance
    return "Unknown", min_distance

# ----------- MAIN ------------
def run_camera_recognition(label_map):
    mean_face, eigvecs, X_projected, labels = load_model(num_components=10)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    print("[*] Mở camera nhận diện... Nhấn Q để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_flat = preprocess_face_from_frame(gray, (x, y, w, h))
            face_proj = project_face(face_flat, mean_face, eigvecs)
            name, distance = recognize_face_from_projection(face_proj, X_projected, labels, label_map, threshold=1500)
            # Hiển thị kết quả
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.putText(frame, f"{name} ({distance:.2f})", (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.imshow("Camera - Nhan dien khuon mat", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[✓] Đã tắt camera.")
def build_label_map(dataset_path="dataset"):
    label_map = {}
    subfolders = sorted(os.listdir(dataset_path))
    for idx, folder in enumerate(subfolders):
        if os.path.isdir(os.path.join(dataset_path, folder)):
            label_map[folder] = idx
    return label_map
# ---------- Label map ----------
label_map = build_label_map("dataset")

if __name__ == "__main__":
    run_camera_recognition(label_map)
