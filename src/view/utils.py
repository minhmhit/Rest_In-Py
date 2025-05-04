import cv2
import os
import tkinter as tk
from tkinter import messagebox

phone_camera_url = 'http://192.168.1.172:4747/video' # <--- **REPLACE THIS URL**

def capture_customer_image(customer_id: str) -> bool:
    if not customer_id:
        print("[!] Customer name is empty, cannot save image.")
        return False

    # Define the absolute directory path
    project_root = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(project_root, "dataset", customer_id.replace(" ", "_"))
    print(f"[*] Attempting to create directory (absolute): {dataset_dir}")

    # Create the directory if it doesn't exist
    try:
        os.makedirs(dataset_dir, exist_ok=True)
        print(f"[*] Successfully created or ensured directory exists (absolute): {dataset_dir}")
    except OSError as e:
        print(f"[!] Error creating directory {dataset_dir}: {e}")
        messagebox.showerror("Lỗi Tạo Thư Mục", f"Không thể tạo thư mục để lưu ảnh:\n{e}")
        return False

    # Check if the directory was actually created
    if not os.path.exists(dataset_dir):
        print(f"[!] WARNING: Directory '{dataset_dir}' does not exist after attempting to create it!") # Added check
        messagebox.showerror("Lỗi Thư Mục", f"Không thể tạo thư mục: '{dataset_dir}'")
        return False

    # Find the next available image number
    image_number = 1
    while True:
        image_path = os.path.join(dataset_dir, f"image_{image_number}.png")
        if not os.path.exists(image_path):
            break
        image_number += 1

    print(f"[*] Next available image number: {image_number}")
    print(f"[*] Attempting to save image to (absolute): {image_path}")

    # Initialize the camera
    cap = cv2.VideoCapture(phone_camera_url)

    if not cap.isOpened():
        print("[!] Error: Could not open camera.")
        messagebox.showerror("Lỗi Camera", "Không thể truy cập camera. Vui lòng kiểm tra kết nối và quyền truy cập.")
        return False

    print("[*] Camera opened. Press 'c' to capture, 'q' to quit.")

    # Create a window to display the camera feed
    window_name = f"Chụp ảnh cho {customer_id} (Nhấn 'c' để chụp, 'q' để thoát)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    captured_frame = None
    success = False

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("[!] Error: Can't receive frame (stream end?). Exiting ...")
            messagebox.showerror("Lỗi Camera", "Không nhận được khung hình từ camera.")
            break

        # Display the frame
        cv2.imshow(window_name, frame)

        # Wait for a key press
        key = cv2.waitKey(1) & 0xFF

        # Check if 'c' is pressed (capture)
        if key == ord('c'):
            captured_frame = frame
            print("[*] 'c' pressed. Capturing image.")
            break  # Exit the loop after capturing

        # Check if 'q' is pressed (quit)
        elif key == ord('q'):
            print("[*] 'q' pressed. Quitting camera.")
            break  # Exit the loop without capturing

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("[*] Camera released and OpenCV windows closed.")

    # Save the captured image if a frame was captured
    if captured_frame is not None:
        print(f"[*] Type of captured_frame before saving: {type(captured_frame)}")
        try:
            cv2.imwrite(image_path, captured_frame)
            print(f"[✓] Image saved successfully to (absolute): {image_path}")
            success = True
        except Exception as e:
            print(f"[!] Error saving image to {image_path}: {e}")
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể lưu ảnh:\n{e}")
            success = False
    else:
        print("[!] No frame was captured, so no image was saved.")

    return success
