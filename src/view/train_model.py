import os
import numpy as np
from PIL import Image
IMAGE_SIZE = (100, 100)
def load_images(dataset_path):
    images = []
    labels = []
    label_map = {}
    label_count = 0
    for person in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person)
        if not os.path.isdir(person_path):
            continue
        if person not in label_map:
            label_map[person] = label_count
            label_count += 1
        for file in os.listdir(person_path):
            if file.endswith(".jpg"):
                img_path = os.path.join(person_path, file)
                img = Image.open(img_path).convert('L').resize(IMAGE_SIZE)
                img_array = np.asarray(img, dtype=np.uint8).flatten()
                images.append(img_array)
                labels.append(label_map[person])
    return np.array(images).T, np.array(labels), label_map

def train_eigenfaces(X):
    mean_face = np.mean(X, axis=1, keepdims=True)
    A = X - mean_face
    cov_matrix = np.dot(A.T, A)

    eigvals, eigvecs_small = np.linalg.eigh(cov_matrix)
    idx = np.argsort(-eigvals)
    eigvecs_small = eigvecs_small[:, idx]
    eigvecs = np.dot(A, eigvecs_small)
    eigvecs = eigvecs / np.linalg.norm(eigvecs, axis=0)
    return mean_face, eigvecs, A

def project_face(face, mean_face, eigvecs, num_components=10):
    face_diff = face.reshape(-1, 1) - mean_face
    projection = np.dot(eigvecs[:, :num_components].T, face_diff)
    return projection

dataset_path = "dataset"
X, y, label_map = load_images(dataset_path)
mean_face, eigvecs, A = train_eigenfaces(X)

np.save("mean_face.npy", mean_face)
np.save("eigvecs.npy", eigvecs)
np.save("X_projected.npy", np.dot(eigvecs.T, A))
np.save("labels.npy", y)
print("Training xong! Đã lưu mô hình.")
