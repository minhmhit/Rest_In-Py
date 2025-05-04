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
    try:
        for person in os.listdir(dataset_path):
            person_path = os.path.join(dataset_path, person)
            if not os.path.isdir(person_path):
                continue
            if person not in label_map:
                label_map[person] = label_count
                label_count += 1
            for file in os.listdir(person_path):
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    img_path = os.path.join(person_path, file)
                    try:
                        img = Image.open(img_path).convert('L').resize(IMAGE_SIZE)
                        img_array = np.asarray(img, dtype=np.uint8).flatten()
                        images.append(img_array)
                        labels.append(label_map[person])
                    except Exception as e:
                        print(f"Error loading image {img_path}: {e}")
    except FileNotFoundError:
        print(f"Error: Dataset directory not found at '{dataset_path}'")
        return np.array([]).T, np.array([]), {}
    except Exception as e:
        print(f"Error loading images from '{dataset_path}': {e}")
        return np.array([]).T, np.array([]), {}
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
# def train_model_thread(dataset_path="dataset"): # Accept dataset_path as argument
#     try:
#         X, y, label_map = load_images(dataset_path)
#         if X.size > 0: # Only train if there are images
#             mean_face, eigvecs, A = train_eigenfaces(X)
#             np.save("mean_face.npy", mean_face)
#             np.save("eigvecs.npy", eigvecs)
#             np.save("X_projected.npy", np.dot(eigvecs.T, A))
#             np.save("labels.npy", y)
#             print("Training completed!")
#         else:
#             print("No images found in the dataset to train.")
#     except Exception as e:
#         print("Training failed:", e)

def train_model_thread(dataset_path="dataset"): # Accept dataset_path as argument
    try:
        X, y, label_map = load_images(dataset_path)
        if X.size > 0: # Only train if there are images
            mean_face, eigvecs, A = train_eigenfaces(X)

            # Define the directory to save .npy files (src/view)
            output_dir = os.path.dirname(os.path.abspath(__file__))

            # Construct the full file paths for saving
            mean_face_path = os.path.join(output_dir, "mean_face.npy")
            eigvecs_path = os.path.join(output_dir, "eigvecs.npy")
            x_projected_path = os.path.join(output_dir, "X_projected.npy")
            labels_path = os.path.join(output_dir, "labels.npy")

            np.save(mean_face_path, mean_face)
            np.save(eigvecs_path, eigvecs)
            np.save(x_projected_path, np.dot(eigvecs.T, A))
            np.save(labels_path, y)

            print(f"Training completed! Model files saved to: {output_dir}")
        else:
            print("No images found in the dataset to train.")
    except Exception as e:
        print("Training failed:", e)

# split thread for training dataset
def start_training(dataset_path="dataset"): # Accept dataset_path as argument
    threading.Thread(target=train_model_thread, args=(dataset_path,), daemon=True).start()

# --- REMOVE OR COMMENT OUT THE FOLLOWING LINES ---
# dataset_path = "dataset"
# X, y, label_map = load_images(dataset_path)
# mean_face, eigvecs, A = train_eigenfaces(X)
# np.save("mean_face.npy", mean_face)
# np.save("eigvecs.npy", eigvecs)
# np.save("X_projected.npy", np.dot(eigvecs.T, A))
# np.save("labels.npy", y)
# print("Training xong! Đã lưu mô hình.")
