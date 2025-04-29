import numpy as np
import cv2
from PIL import Image # Imported but not used in the provided code
import os

CURRENT_DIR = os.path.dirname(__file__) # Directory of this file (src/view/)

# Path to the AI directory relative to the current directory
AI_DIR_RELATIVE = os.path.join(CURRENT_DIR, '..', 'AI')

# Construct paths to resource files inside the AI directory
DATASET_PATH = os.path.join(AI_DIR_RELATIVE, "dataset")
TRAINER_FILE = os.path.join(AI_DIR_RELATIVE, "trainer.yml")
MEAN_FACE_FILE = os.path.join(AI_DIR_RELATIVE, "mean_face.npy")
EIGVECS_FILE = os.path.join(AI_DIR_RELATIVE, "eigvecs.npy")
X_PROJECTED_FILE = os.path.join(AI_DIR_RELATIVE, "X_projected.npy")
LABELS_FILE = os.path.join(AI_DIR_RELATIVE, "labels.npy")
# Assuming haarcascade is also in src/AI/
HAARCASCADE_FILE = os.path.join(AI_DIR_RELATIVE, 'haarcascade_frontalface_default.xml')
# If you want to use the one installed with OpenCV (less reliable sometimes):
# HAARCASCADE_BUILTIN = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'


IMAGE_SIZE = (100, 100) # Standardize face image size

# --- Functions matching the requested import names ---
# These functions will use the correctly calculated paths defined above

def load_model(num_components=10):
    print("[*] Loading face recognition model components...")
    mean_face, eigvecs, X_projected, labels = None, None, None, None

    # Load Eigenfaces components - add checks for file existence
    try:
        if not os.path.exists(MEAN_FACE_FILE): raise FileNotFoundError(f"Mean face file not found at {MEAN_FACE_FILE}")
        if not os.path.exists(EIGVECS_FILE): raise FileNotFoundError(f"Eigenvectors file not found at {EIGVECS_FILE}")
        if not os.path.exists(X_PROJECTED_FILE): raise FileNotFoundError(f"Projected data file not found at {X_PROJECTED_FILE}")
        if not os.path.exists(LABELS_FILE): raise FileNotFoundError(f"Labels file not found at {LABELS_FILE}")

        mean_face = np.load(MEAN_FACE_FILE)
        eigvecs = np.load(EIGVECS_FILE)
        X_projected = np.load(X_PROJECTED_FILE)
        labels = np.load(LABELS_FILE)

        # Apply number of components
        if num_components > eigvecs.shape[1]:
             print(f"Warning: num_components ({num_components}) is greater than available eigenvectors ({eigvecs.shape[1]}). Using available.")
             num_components = eigvecs.shape[1]
        if num_components > X_projected.shape[0]:
             print(f"Warning: num_components ({num_components}) is greater than available projected dimensions ({X_projected.shape[0]}). Using available.")
             num_components = X_projected.shape[0]


        X_projected = X_projected[:num_components, :]
        eigvecs = eigvecs[:, :num_components]


        print("[✓] Loaded Eigenfaces components.")

    except FileNotFoundError as e:
        print(f"[!] Error: {e}. Please ensure training has been completed successfully and model files are in the AI directory.")
        # Return None for all components if core files are missing
        return None, None, None, None, None
    except Exception as e:
        print(f"[!] Error loading Eigenfaces components: {e}")
        return None, None, None, None, None

    # Load Haar Cascade classifier - add checks for file existence
    if not os.path.exists(HAARCASCADE_FILE):
         print(f"[!] Error: Haar Cascade file not found at {HAARCASCADE_FILE}.")
         print("    Ensure the file exists in the AI directory or update HAARCASCADE_FILE path.")
         face_cascade = None
    else:
        face_cascade = cv2.CascadeClassifier(HAARCASCADE_FILE) # Use the defined path
        if face_cascade.empty():
             print(f"[!] Error: Could not load Haar Cascade classifier from {HAARCASCADE_FILE}.")
             print("    Ensure opencv-contrib-python is installed correctly or the file is valid.")
             face_cascade = None
        else:
             print("[✓] Loaded Haar Cascade classifier.")


    return mean_face, eigvecs, X_projected, labels, face_cascade


def build_label_map(dataset_directory=DATASET_PATH):
    print(f"[*] Building label map from {dataset_directory}...")
    label_map = {}
    if not os.path.exists(dataset_directory):
        print(f"[!] Warning: Dataset directory not found at {dataset_directory}. Label map will be empty.")
        return label_map # Return empty map if directory doesn't exist

    try:
        # List subdirectories (each representing a person/label)
        # Sort to ensure consistent label mapping (important for training/recognition consistency)
        subfolders = sorted([d for d in os.listdir(dataset_directory) if os.path.isdir(os.path.join(dataset_directory, d))])

        # The original code's label map seems reversed based on typical usage (name: id)
        # Reversing it to {id: name} for easier lookup by prediction label
        label_map = {idx: folder for idx, folder in enumerate(subfolders)}

        print(f"[✓] Built label map: {label_map}")
        return label_map
    except Exception as e:
        print(f"[!] Error building label map from {dataset_directory}: {e}")
        return {}


def preprocess_face_from_frame(gray_frame, face_coords):
    if gray_frame is None or face_coords is None or len(face_coords) != 4:
         return None

    x, y, w, h = face_coords

    try:
        # Ensure bounds are within the frame
        y = max(0, y)
        x = max(0, x)
        h = min(h, gray_frame.shape[0] - y)
        w = min(w, gray_frame.shape[1] - x)
        if w <= 0 or h <= 0: # Check if dimensions are valid
             return None

        face_img = gray_frame[y:y+h, x:x+w]
        face_resized = cv2.resize(face_img, IMAGE_SIZE)
        # Ensure image is the correct type (CV_8U) if needed
        # face_resized = np.array(face_resized, 'uint8')
        return face_resized
    except Exception as e:
         print(f"[!] Error preprocessing face from coords {face_coords}: {e}")
         return None


def project_face(face_resized_flat, mean_face, eigvecs):
    if face_resized_flat is None or mean_face is None or eigvecs is None:
        return None
    # Ensure face_resized_flat is a column vector (shape (N, 1))
    if face_resized_flat.ndim == 1:
        face_resized_flat = face_resized_flat.reshape(-1, 1)
    elif face_resized_flat.shape[1] != 1:
        print(f"[!] Warning: face_resized_flat not a column vector, reshaping. Shape: {face_resized_flat.shape}")
        face_resized_flat = face_resized_flat.flatten().reshape(-1, 1)


    try:
        face_diff = face_resized_flat - mean_face.reshape(-1, 1) # Ensure mean_face is also a column vector
        projection = np.dot(eigvecs.T, face_diff) # eigvecs shape (N*M, num_components), need transpose for dot product
        return projection
    except Exception as e:
         print(f"[!] Error projecting face: {e}")
         return None


def recognize_face_from_projection(face_proj, X_projected, labels, label_map, threshold=1500):
    if face_proj is None or X_projected is None or labels is None or not label_map:
        return "Unknown", float('inf') # Cannot recognize without valid inputs

    # Ensure face_proj is a column vector for distance calculation
    if face_proj.ndim == 1:
        face_proj = face_proj.reshape(-1, 1)

    try:
        # Calculate Euclidean distances to all projected training images
        # Need to compare the face_proj (column vector) to each column in X_projected
        # X_projected shape is (num_components, num_training_images)
        # face_proj shape is (num_components, 1)
        # Use axis=0 for norm over the feature dimension
        distances = np.linalg.norm(X_projected - face_proj, axis=0)


        if distances.size == 0: # Handle case with no training data
             return "Unknown", float('inf')

        best_match_idx = np.argmin(distances)
        min_distance = distances[best_match_idx]

        if min_distance > threshold:
            return "Unknown", min_distance # Not recognized

        # Find the label of the best match
        predicted_label = labels[best_match_idx]

        # Look up the name using the label map (which is {id: name})
        predicted_name = label_map.get(predicted_label, f"Unknown (ID:{predicted_label})")

        return predicted_name, min_distance

    except Exception as e:
        print(f"[!] Error during face recognition prediction: {e}")
        return "Error", float('inf') # Handle prediction errors


# You might want to keep the draw function from previous versions, but it wasn't in your original import list
# Adding it here as it's useful for visualization
def draw_prediction_on_frame(frame, name, distance, x, y, w, h, threshold=1500, color=(0, 255, 0)):
    """Draws the bounding box and prediction text on the frame."""
    # Decide color based on recognition status
    display_color = (0, 255, 0) # Green for recognized
    if name == "Unknown" or name == "Error" or distance > threshold:
        display_color = (0, 0, 255) # Red for unknown or error

    cv2.rectangle(frame, (x, y), (x + w, y + h), display_color, 2)

    # Text to display
    display_text = name
    if name != "Unknown" and name != "Error":
        display_text += f" ({distance:.2f})" # Show distance for known faces

    # Position text above the rectangle
    text_y = y - 10 if y - 10 > 10 else y + 10 # Avoid drawing off-screen top
    cv2.putText(frame, display_text, (x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, display_color, 2)


# ----------- Main Execution Function (to be called from elsewhere) ------------
def run_camera_recognition(label_map):
    """
    Initializes components, opens camera, and runs the face recognition loop.
    This function should be called by the main application logic (e.g., in camera.py).

    Args:
        label_map (dict): The label map ({id: name}).
    """
    print("[*] Starting camera recognition...")

    # Load necessary components using the defined functions
    # This will handle paths and basic loading errors
    mean_face, eigvecs, X_projected, labels, face_cascade = load_model(num_components=10)

    # Check if loading was successful and label map is valid
    if mean_face is None or eigvecs is None or X_projected is None or labels is None or face_cascade is None or not label_map:
        print("[!] Failed to load all required components or label map is empty. Cannot start recognition.")
        print("    Ensure model files exist, cascade loads, dataset is not empty, and label map is built.")
        return # Exit the function if loading failed

    cap = cv2.VideoCapture(0) # Open webcam (or specify video file path)
    if not cap.isOpened():
        print("[!] Error: Could not open webcam.")
        return # Exit the function if webcam fails to open

    print("[✓] Camera opened. Press 'q' to quit.")

    # Get the recognition threshold from the model loading if needed, or use default
    recognition_threshold = 1500 # Use the default threshold for now

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[!] Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Convert frame to grayscale for face detection and preprocessing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        # Returns a list of rectangles (x, y, w, h)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Add quit instruction text
        cv2.putText(frame, "Press 'q' to quit", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)


        for (x, y, w, h) in faces:
            # --- Recognition Pipeline for each detected face ---

            # 1. Preprocess the detected face region (extract ROI and resize)
            face_resized = preprocess_face_from_frame(gray, (x, y, w, h))

            if face_resized is not None:
                # Flatten the resized face image
                face_flat = face_resized.flatten() # No need for reshape(-1, 1) here, project_face handles it

                # 2. Project the face onto the eigenvector space
                face_proj = project_face(face_flat, mean_face, eigvecs)

                if face_proj is not None:
                    # 3. Recognize the face from the projection (compare to training data)
                    name, distance = recognize_face_from_projection(face_proj, X_projected, labels, label_map, threshold=recognition_threshold)

                    # 4. Draw the results on the original color frame
                    draw_prediction_on_frame(frame, name, distance, x, y, w, h, threshold=recognition_threshold)
            # --- End Recognition Pipeline ---


        # Display the resulting frame with detections/predictions
        cv2.imshow("Camera - Nhan dien khuon mat", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    print("[✓] Camera and windows closed.")

if __name__ == "__main__":
    print("Running recognize_faces.py as a standalone recognition script test.")

    label_map = build_label_map(DATASET_PATH) # Corrected call to use the constant

    if not label_map:
        print("[!] Cannot run recognition without a label map. Ensure dataset exists and is not empty.")
    else:
        run_camera_recognition(label_map)

    print("Standalone script finished.")
