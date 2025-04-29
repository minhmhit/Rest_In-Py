import random
# import string # Not used
import tkinter as tk
import cv2
import numpy as np # Use np consistently
from PIL import Image, ImageTk
from datetime import datetime
import time
import os # Import os for path joining

# Import the necessary functions from the refactored recognize_faces module
# The import path assumes recognize_faces.py is in the same 'view' directory
# If recognize_faces.py is in src/AI/, the import should be from AI.recognize_faces import ...
# Based on the last traceback, it's in src/view/.
from view.recognize_faces import load_model, build_label_map, preprocess_face_from_frame, project_face, recognize_face_from_projection, draw_prediction_on_frame # Assuming draw_prediction_on_frame is also needed

# --- Define paths for resources directly used by camera.py ---
# If camera.py needs to load files directly, define paths relative to camera.py
# Assuming the haarcascade file is in src/AI/
# To get from src/view/camera.py to src/AI/haarcascade_frontalface_default.xml:
# Go up one level ('..') to src/, then down into 'AI', then specify the filename
CAMERA_DIR = os.path.dirname(__file__) # Directory of this file (src/view/)
HAARCASCADE_CAMERA_PATH = os.path.join(CAMERA_DIR, '..', 'view', 'haarcascade_frontalface_default.xml')

# Define the threshold for recognition distance
RECOGNITION_THRESHOLD = 1500

# Define a color constant for background
BG_COLOR = "#F5F5F5"


class Camera(tk.Frame):

    def __init__(self, parent):
        self.notifications = []
        super().__init__(parent, bg=BG_COLOR)

        # --- Recognition Components ---
        # Load these components once when the Camera object is initialized
        print("[*] Initializing face recognition components in Camera...")
        # load_model and build_label_map handle their internal paths (relative to recognize_faces.py)
        self.mean_face, self.eigvecs, self.X_projected, self.labels, self.face_cascade_loaded_via_model = load_model(num_components=10)
        self.label_map = build_label_map()

        # Also load the cascade classifier directly in camera.py if needed for detection
        # Using the path defined relative to camera.py
        self.face_cascade = cv2.CascadeClassifier(HAARCASCADE_CAMERA_PATH)


        # Store recognition components together and check if loading was successful
        self.recognition_components = (self.mean_face, self.eigvecs, self.X_projected, self.labels)

        self.recognition_enabled = (
            # self.cap is initialized later
            self.face_cascade is not None and not self.face_cascade.empty() and # Cascade loaded in Camera
            all(comp is not None for comp in self.recognition_components) and # All Eigenfaces components loaded
            bool(self.label_map) # Label map is not empty
        )

        if not self.recognition_enabled:
            print("[!] Face recognition will be disabled due to loading errors or missing components.")
            print("    Ensure model files (.npy, .yml), cascade XML, and dataset are in src/AI/")
            # Ensure components are None if not enabled to prevent errors later
            self.recognition_components = (None, None, None, None)
            self.label_map = {}
            self.face_cascade = None # Use the one loaded locally, set to None if it failed

        # --- Camera Setup ---
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("[!] Error: Could not open webcam in Camera.__init__.")
            self.running = False # Stop the update loop flag
            self.cap = None # Set to None to avoid errors
            # If camera fails, recognition is also not possible
            self.recognition_enabled = False
            # Maybe show an error message in the UI immediately


        # run flag for update_frame loop
        self.running = True # Set to True if camera opened, False otherwise
        if self.cap is None: self.running = False

        self.after_id = None # For managing Tkinter's after calls

        # --- UI Setup ---
        # Use BG_COLOR constant
        self.mainPanel = tk.LabelFrame(self, bg="white") # Keep main panel white for camera feed
        self.leftPanel = tk.LabelFrame(self, bg=BG_COLOR) # Left panel background

        # configure weights for main Camera frame columns
        # Adjusted weights: Left panel (column 0) gets weight 1, Main panel (column 1) gets weight 7
        self.columnconfigure(0, weight=1) # Left panel (smaller)
        self.columnconfigure(1, weight=7) # Main panel (larger)
        self.rowconfigure(0, weight=1) # Only one row, make it expand

        # place LabelFrames
        self.leftPanel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) # Added padding
        self.mainPanel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5) # Added padding

        # --- Main Panel Widgets ---
        self.title_video = tk.Label(
            self.mainPanel,
            bg=BG_COLOR, # Using BG_COLOR constant
            fg="black",
            text="Camera Sảnh Chính",
            font=("Arial", 20, "bold"),
            anchor="center",
            justify="center",
            bd=0,
            padx=10,
            pady=10,
        )
        # Label to display the camera feed (initially empty)
        self.show_camera = tk.Label(
            self.mainPanel, bg="black", bd=0 # Black background for camera area
            # Do NOT set height/width fixed here if using sticky="nsew" and weights
            # Let grid/pack manage size, or set minimum size if needed
        )

        # Main panel weights for internal widgets
        self.mainPanel.rowconfigure(0, weight=0) # Title row doesn't expand vertically
        self.mainPanel.rowconfigure(1, weight=1) # Camera feed row expands vertically
        self.mainPanel.columnconfigure(0, weight=1) # Single column expands horizontally

        # Place main panel widgets
        self.title_video.grid(row=0, column=0, sticky="nsew")
        self.show_camera.grid(row=1, column=0, sticky="nsew") # Use sticky to make it fill


        # --- Left Panel Widgets (Notifications) ---
        # Add a title for the notification box
        self.notification_title = tk.Label(
            self.leftPanel,
            bg=BG_COLOR,
            fg="black",
            text="Thông báo nhận diện", # Title for notifications
            font=("Arial", 12, "bold"),
            anchor="w", # Align text to the west (left)
            padx=10,
            pady=5
        )

        self.notification_box = tk.Text(
            self.leftPanel,
            height=5, # Height in text lines (can be overridden by grid/pack)
            # width=10, # Width in characters (can be overridden)
            bg="white", # White background for text box
            fg="black",
            state="disabled", # Start as disabled
            bd=1, # Add a small border
            padx=5,
            pady=5,
            wrap="word" # Wrap text by word
        )
         # Left panel weights for internal widgets
        self.leftPanel.rowconfigure(0, weight=0) # Title row doesn't expand vertically
        self.leftPanel.rowconfigure(1, weight=1) # Notification box row expands vertically
        self.leftPanel.columnconfigure(0, weight=1) # Single column expands horizontally

        # Place left panel widgets using grid
        self.notification_title.grid(row=0, column=0, sticky="nsew") # Place title at top
        self.notification_box.grid(row=1, column=0, sticky="nsew") # Place text box below title and make it fill


        # --- Recognition Logging ---
        self.last_logged_times = {} # {name: timestamp} to track last log time for each person
        # Ensure timelog.txt path is correct relative to where main.py is run
        # If timelog.txt is in the project root (where you run python src/main.py)
        self.timelog_file_path = "view/timelog.txt"


        # --- Start Update Loop ---
        # Only start the update loop if the camera successfully opened
        if self.running:
             self.update_frame() # Start the frame update loop
        else:
             print("[!] Camera not opened. update_frame loop will not start.")
             # You might want to display an error message in the UI here


    # --- Notification Methods ---
    # (Your existing notification methods)

    def remove_oldest_notifications(self):
        """Removes the oldest notification if the list is not empty."""
        if self.notifications:
            print(f"[*] Removing oldest notification: {self.notifications[0]}")
            self.notifications.pop(0) # remove first (oldest) item
            self.update_notifications()

    def update_notifications(self):
        """Updates the text box widget with the current notifications."""
        self.notification_box.config(state="normal") # Enable editing temporarily
        self.notification_box.delete("1.0", tk.END) # Clear all text

        # Insert new notifications first (newest at the top)
        # Join messages with newlines; notifications are stored oldest first, so reverse for newest-first display
        new_text = "\n".join(self.notifications[::-1])
        self.notification_box.insert("1.0", new_text) # Insert all at the beginning

        self.notification_box.config(state="disabled") # Disable editing


    # --- Camera Frame Update Function ---
    def update_frame(self):
        """Reads a frame from the camera, performs recognition, and updates the Tkinter Label."""
        if not self.running:
            # Cleanup when the loop is stopping
            print("[*] Stopping update_frame loop.")
            if hasattr(self, 'cap') and self.cap is not None and self.cap.isOpened():
                 self.cap.release()
                 print("[✓] Camera released.")
            cv2.destroyAllWindows() # Destroy OpenCV windows
            return # Stop the recursion

        # Get frame from camera
        ret, frame = self.cap.read()
        if not ret:
            print("[!] Error: Can't receive frame from camera. Stopping update_frame.")
            self.running = False  # Stop if no frame
            # Schedule one final call to run the cleanup logic before returning
            self.after_id = self.show_camera.after(10, self.update_frame)
            return


        # --- Perform Recognition (Only if enabled) ---
        # Only attempt face detection and recognition if components loaded
        if self.recognition_enabled:
             # Convert frame to grayscale for face detection and preprocessing
             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

             # Detect faces using the cascade loaded in __init__
             # Use self.face_cascade which is the cascade loaded in camera.py
             faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

             # Get components from stored tuple
             mean_face, eigvecs, X_projected, labels = self.recognition_components


             for (x, y, w, h) in faces:
                 # --- Recognition Pipeline for each detected face ---

                 # 1. Preprocess the detected face region (extract ROI and resize)
                 # Call imported function from recognize_faces.py
                 face_resized = preprocess_face_from_frame(gray, (x, y, w, h))

                 if face_resized is not None:
                      face_flat = face_resized.flatten() # Flatten the resized face image

                      # 2. Project the face onto the eigenvector space
                      # Call imported function from recognize_faces.py
                      face_proj = project_face(face_flat, mean_face, eigvecs)

                      if face_proj is not None:
                           # 3. Recognize the face from the projection (compare to training data)
                           # Call imported function from recognize_faces.py
                           name, distance = recognize_face_from_projection(face_proj, self.X_projected, self.labels, self.label_map, threshold=RECOGNITION_THRESHOLD) # Use the defined threshold constant

                           # 4. Draw the results on the original color frame
                           # Use the imported draw function
                           draw_prediction_on_frame(frame, name, distance, x, y, w, h, threshold=RECOGNITION_THRESHOLD) # Pass threshold to drawing function
                           self.log_recognition(name) # Log the name if recognized
             # Log recognition results after processing all faces in the frame
             # This might log multiple times per person if they appear in multiple frames
             # Consider logging only once per person per time interval in log_recognition
             # (The current log_recognition already handles the time interval)
             # No need to call log_recognition here inside the face loop, it's called within update_frame



        # --- End Recognition ---
        else:
            # If recognition is not enabled, you might still want to draw faces or show a message
            # Or just display the raw camera feed.
            # You can still detect faces if self.face_cascade is loaded, even if recognition data is missing
            if self.face_cascade is not None and not self.face_cascade.empty():
                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                 faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                 for (x, y, w, h) in faces:
                     # Just draw rectangles for detected faces if recognition is off
                     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) # Blue rectangle for detected only
                     cv2.putText(frame, "Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)


        # --- Display Frame in Tkinter ---
        # Convert the OpenCV frame (BGR) to RGB for PIL
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)

        # Resize image to fit the Label widget size
        # Get current size of the label widget
        label_width = self.show_camera.winfo_width()
        label_height = self.show_camera.winfo_height()

        # Only resize if the label has a valid size (might be 0 before window is displayed)
        # This logic makes the image fill the label's space, potentially stretching it if aspect ratios differ
        if label_width > 0 and label_height > 0:
            img = img.resize((label_width, label_height), Image.Resampling.LANCZOS) # Use LANCZOS for better quality resize
        # If you want to maintain aspect ratio and center, the logic would be different:
        # frame_h, frame_w, _ = frame.shape
        # aspect_ratio = frame_w / frame_h
        # target_w = label_width
        # target_h = int(target_w / aspect_ratio)
        # if target_h > label_height:
        #     target_h = label_height
        #     target_w = int(target_h * aspect_ratio)
        # img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        # # Then potentially center the image within the label

        imgtk = ImageTk.PhotoImage(image=img)

        self.show_camera.imgtk = imgtk # Keep a reference to prevent garbage collection
        self.show_camera.config(image=imgtk) # Update the Label's image


        # Schedule the next frame update after 10ms
        self.after_id = self.show_camera.after(10, self.update_frame)


    # --- Log Recognition Method ---
    def log_recognition(self, name):
        """Logs recognized names to a file and updates the notification box."""
        # Only log if name is recognized (not "Unknown", "Error", or empty)
        if not name or name in ["Unknown", "Error"]:
             return # Don't log unknown or errors

        now = time.time()
        last_time = self.last_logged_times.get(name, 0)
        # Log only if 10 seconds have passed since the last log for this name
        if now - last_time >= 10:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"Nhận diện: {name} vào lúc [{timestamp}]\n"
            try:
                # Write to the timelog file
                with open(self.timelog_file_path, "a", encoding="utf-8") as f:
                    f.write(log_entry)
                print(f"[✓] Logged recognition: {log_entry.strip()}") # Print to console for feedback
            except Exception as e:
                print(f"[!] Error writing to {self.timelog_file_path}: {e}")


            # Add to notification box
            notification_text = f"🎯 Nhận diện: {name} vào lúc [{timestamp}] "
            self.notifications.append(notification_text)

            # Optional: Limit the number of notifications shown (e.g., last 10)
            max_notifications = 10
            while len(self.notifications) > max_notifications:
                self.notifications.pop(0) # Remove the oldest notification

            # Update the notification text box UI
            self.update_notifications()

            # Update the last logged time for this name
            self.last_logged_times[name] = now


    # --- Cleanup Method ---
    # This method is called when the Camera object is likely being destroyed (e.g., window closed)
    def __del__(self):
        """Cleans up camera and OpenCV resources."""
        print("[*] Cleaning up Camera object resources...")
        self.running = False # Ensure the update loop stops
        # Cancel any pending after calls
        if self.after_id is not None and hasattr(self.show_camera, 'after_cancel'):
            self.show_camera.after_cancel(self.after_id)
            self.after_id = None
            print("[✓] Cancelled pending Tkinter 'after' calls.")
        # Release the camera
        if hasattr(self, 'cap') and self.cap is not None and self.cap.isOpened():
            self.cap.release()
            print("[✓] Camera released.")
        # Destroy OpenCV windows
        cv2.destroyAllWindows()
        print("[✓] OpenCV windows destroyed.")

    # --- Public Method to Stop Camera (Call this when closing the main window) ---
    def stop_camera(self):
        """Sets the running flag to False to stop the update loop."""
        print("[*] Stop signal received. Camera update loop will stop soon.")
        self.running = False
