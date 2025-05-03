import os
import threading
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
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"): # Added more image extensions
                img_path = os.path.join(person_path, file)
                try:
                    img = Image.open(img_path).convert('L').resize(IMAGE_SIZE)
                    img_array = np.asarray(img, dtype=np.uint8).flatten()
                    images.append(img_array)
                    labels.append(label_map[person])
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")
    return np.array(images).T, np.array(labels), label_map

def train_eigenfaces(X):
    mean_face = np.mean(X, axis=1, keepdims=True)
    A = X - mean_face
    cov_matrix = np.dot(A.T, A)

    eigvals, eigvecs_small = np.linalg.eigh(cov_matrix)
    idx = np.argsort(-eigvals)[::-1] # Sort in descending order
    eigvecs_small = eigvecs_small[:, idx]
    eigvecs = np.dot(A, eigvecs_small)
    eigvecs = eigvecs / np.linalg.norm(eigvecs, axis=0)
    return mean_face, eigvecs, A

def project_face(face, mean_face, eigvecs, num_components=10):
    face_diff = face.reshape(-1, 1) - mean_face
    projection = np.dot(eigvecs[:, :num_components].T, face_diff)
    return projection

# train model after capture new customer image
def train_model_thread(dataset_path="dataset"): # Accept dataset_path as argument
    try:
        X, y, label_map = load_images(dataset_path)
        if X.size > 0: # Only train if there are images
            mean_face, eigvecs, A = train_eigenfaces(X)
            np.save("mean_face.npy", mean_face)
            np.save("eigvecs.npy", eigvecs)
            np.save("X_projected.npy", np.dot(eigvecs.T, A))
            np.save("labels.npy", y)
            print("Training completed!")
        else:
            print("No images found in the dataset to train.")
    except Exception as e:
        print("Training failed:", e)

# split thread for training dataset
def start_training(dataset_path="dataset"): # Accept dataset_path as argument
    threading.Thread(target=train_model_thread, args=(dataset_path,), daemon=True).start()

# --- How to integrate with your image capture function ---
# In your capture_customer_image function (from your previous code),
# after successfully saving an image:

# if success:
#     print("[*] Starting training in a separate thread...")
#     start_training("src/view/dataset") # Pass the correct dataset path

# --- You should remove the following lines from the global scope ---
# dataset_path = "dataset"
# X, y, label_map = load_images(dataset_path)
# mean_face, eigvecs, A = train_eigenfaces(X)
# np.save("mean_face.npy", mean_face)
# np.save("eigvecs.npy", eigvecs)
# np.save("X_projected.npy", np.dot(eigvecs.T, A))
# np.save("labels.npy", y)
# print("Training xong! Đã lưu mô hình.")
