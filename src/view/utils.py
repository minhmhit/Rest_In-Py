import cv2
import os
import tkinter as tk
from tkinter import messagebox

def capture_customer_image(customer_name: str) -> bool:
    if not customer_name:
        print("[!] Customer name is empty, cannot save image.")
        return False

    # Define the directory path based on the customer name
    # Replace spaces with underscores or use a different sanitization if needed
    sanitized_name = customer_name.replace(" ", "_")
    dataset_dir = os.path.join("src", "view", "dataset", sanitized_name)

    # Create the directory if it doesn't exist
    if not os.path.exists(dataset_dir):
        try:
            os.makedirs(dataset_dir)
            print(f"[*] Created directory: {dataset_dir}")
        except OSError as e:
            print(f"[!] Error creating directory {dataset_dir}: {e}")
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể tạo thư mục để lưu ảnh:\n{e}")
            return False

    # Define the image file path
    image_path = os.path.join(dataset_dir, "image.png") # You can change the filename if needed

    # Check if the image file already exists (optional, you might want to overwrite)
    if os.path.exists(image_path):
        print(f"[*] Image file already exists: {image_path}. It will be overwritten.")
        # You could add a confirmation dialog here if you don't want to overwrite automatically

    # Initialize the camera
    # 0 usually refers to the default camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[!] Error: Could not open camera.")
        messagebox.showerror("Lỗi Camera", "Không thể truy cập camera. Vui lòng kiểm tra kết nối và quyền truy cập.")
        return False

    print("[*] Camera opened. Press 'c' to capture, 'q' to quit.")

    # Create a window to display the camera feed
    window_name = f"Chụp ảnh cho {customer_name} (Nhấn 'c' để chụp, 'q' để thoát)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL) # Use WINDOW_NORMAL for resizable window

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
        # waitKey(1) waits for 1ms, allowing the GUI to update
        key = cv2.waitKey(1) & 0xFF

        # Check if 'c' is pressed (capture)
        if key == ord('c'):
            captured_frame = frame
            print("[*] 'c' pressed. Capturing image.")
            break # Exit the loop after capturing

        # Check if 'q' is pressed (quit)
        elif key == ord('q'):
            print("[*] 'q' pressed. Quitting camera.")
            break # Exit the loop without capturing

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("[*] Camera released and OpenCV windows closed.")

    # Save the captured image if a frame was captured
    if captured_frame is not None:
        try:
            # Save the image
            cv2.imwrite(image_path, captured_frame)
            print(f"[✓] Image saved successfully to {image_path}")
            success = True
        except Exception as e:
            print(f"[!] Error saving image to {image_path}: {e}")
            messagebox.showerror("Lỗi Lưu Ảnh", f"Không thể lưu ảnh:\n{e}")
            success = False

    return success

# Example usage (for testing the utility function directly)
# if __name__ == "__main__":
#     # Create a dummy dataset directory structure for testing
#     os.makedirs(os.path.join("src", "view", "dataset", "Test Customer"), exist_ok=True)
#     capture_customer_image("Test Customer")
