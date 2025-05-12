import random
# import string # Not used
import tkinter as tk
import cv2
import numpy as np # Use np consistently
from PIL import Image, ImageTk
from datetime import datetime
import time
import os # Import os for path joining

# Assuming your view.recognize_faces module is structured as provided
# If these functions are in the same directory or accessible via PYTHONPATH, this should work.
# Otherwise, adjust the import path.
# from view.recognize_faces import load_model, build_label_map, preprocess_face_from_frame, project_face, recognize_face_from_projection, draw_prediction_on_frame
# For the purpose of this example, let's create placeholder functions if the module is not available
# In your actual application, REMOVE these placeholders and use your actual import.
try:
    from view.recognize_faces import load_model, build_label_map, preprocess_face_from_frame, project_face, recognize_face_from_projection, draw_prediction_on_frame
except ImportError:
    print("[!] Warning: 'view.recognize_faces' module not found. Using placeholder functions.")
    print("    Please ensure the module is in the correct path for full functionality.")
    # Placeholder functions (replace with your actual implementations)
    def load_model(num_components=10):
        print("[!] Placeholder load_model called.")
        # Simulate loading data: mean_face, eigvecs, X_projected, labels, face_cascade_loaded_via_model
        # These would typically be loaded from .npy files or a model file.
        # For demonstration, we'll return Nones or empty structures.
        # The face_cascade_loaded_via_model is not used in the Camera class directly for detection,
        # but it's good practice to return it if your load_model function does.
        return (None, None, None, None, None) # mean_face, eigvecs, X_projected, labels, face_cascade

    def build_label_map():
        print("[!] Placeholder build_label_map called.")
        # This would typically read from a file or database mapping integer labels to names.
        return {} # Return an empty dictionary

    def preprocess_face_from_frame(gray_frame, face_rect):
        # print("[!] Placeholder preprocess_face_from_frame called.") # Can be noisy
        # (x, y, w, h) = face_rect
        # face_roi = gray_frame[y:y+h, x:x+w]
        # face_resized = cv2.resize(face_roi, (100, 100), interpolation=cv2.INTER_LANCZOS4) # Example size
        return np.zeros((100, 100), dtype=np.uint8) # Return a dummy resized face for processing

    def project_face(face_flat, mean_face, eigvecs):
        # print("[!] Placeholder project_face called.") # Can be noisy
        # Simulate a projection if mean_face and eigvecs were actual data
        if mean_face is not None and eigvecs is not None:
             # This is a simplification; actual projection involves subtraction and dot product
            return np.zeros(eigvecs.shape[0]) # Dummy projection of correct dimension
        return None

    def recognize_face_from_projection(face_proj, X_projected, labels, label_map, threshold):
        # print("[!] Placeholder recognize_face_from_projection called.") # Can be noisy
        return "Placeholder", 0.0 # Return dummy name and distance

    def draw_prediction_on_frame(frame, name, distance, x, y, w, h, threshold):
        # print("[!] Placeholder draw_prediction_on_frame called.") # Can be noisy
        color = (0, 255, 0) if name != "Unknown" and name != "Placeholder" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        text = f"{name} ({distance:.2f})" if name != "Placeholder" else name
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        pass


CAMERA_DIR = os.path.dirname(__file__)
# Try to construct a more robust path for HAARCASCADE_CAMERA_PATH
# Assuming 'camera.py' is in 'src/view/' and 'haarcascade_frontalface_default.xml' is also in 'src/view/'
HAARCASCADE_CAMERA_PATH = os.path.join(CAMERA_DIR, 'haarcascade_frontalface_default.xml')

if not os.path.exists(HAARCASCADE_CAMERA_PATH):
    # Fallback: If 'camera.py' is in 'src/controller' and 'haarcascade_frontalface_default.xml' is in 'src/view/'
    HAARCASCADE_CAMERA_PATH = os.path.join(CAMERA_DIR, '..', 'view', 'haarcascade_frontalface_default.xml')

if not os.path.exists(HAARCASCADE_CAMERA_PATH):
    print(f"[!] Critical Error: Haar cascade file not found after checking multiple common paths.")
    print(f"    Attempted: {os.path.join(CAMERA_DIR, 'haarcascade_frontalface_default.xml')}")
    print(f"    Attempted: {os.path.join(CAMERA_DIR, '..', 'view', 'haarcascade_frontalface_default.xml')}")
    print("    Please ensure 'haarcascade_frontalface_default.xml' is correctly located relative to your script or provide an absolute path.")
    print("    Face detection will likely fail. Trying OpenCV default path as a last resort.")
    # Fallback: try to load from a common OpenCV path if available (less reliable)
    HAARCASCADE_CAMERA_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    if not os.path.exists(HAARCASCADE_CAMERA_PATH):
        print(f"[!] Critical Error: Also failed to find Haar cascade at OpenCV default path: {HAARCASCADE_CAMERA_PATH}")
        HAARCASCADE_CAMERA_PATH = "" # Set to empty to make cascade loading fail clearly


# Define the threshold for recognition distance
RECOGNITION_THRESHOLD = 1500 # Example, adjust based on your Eigenfaces implementation

# Define a color constant for background
BG_COLOR = "#F5F5F5"


class Camera(tk.Frame):

    def __init__(self, parent):
        self.notifications = []
        super().__init__(parent, bg=BG_COLOR)

        # --- Initialize core attributes that reload_model_data might check ---
        self.cap = None # Initialize cap to None first
        self.face_cascade = None # Initialize face_cascade to None

        # --- Recognition Components (will be initialized by reload_model_data) ---
        self.mean_face = None
        self.eigvecs = None
        self.X_projected = None
        self.labels = None
        # self.face_cascade_loaded_via_model = None # From load_model, if your load_model returns it
        self.label_map = {}
        self.recognition_components = ()
        self.recognition_enabled = False # Default to False

        # --- Camera Setup (Initialize self.cap BEFORE calling reload_model_data) ---
        print("[*] Initializing webcam...")
        self.cap = cv2.VideoCapture(0) # Try to initialize camera
        if not self.cap.isOpened():
            print("[!] Error: Could not open webcam in Camera.__init__.")
            self.running = False # Stop the update loop flag
            # self.cap remains None, which reload_model_data will check
            self.recognition_enabled = False # If camera fails, recognition is also not possible
        else:
            self.running = True # Set to True if camera opened
            print("[✓] Webcam opened successfully.")

        # --- Haar Cascade Setup (Initialize self.face_cascade BEFORE calling reload_model_data) ---
        # This cascade is used for detection in the camera feed.
        print(f"[*] Loading Haar Cascade for face detection from: {HAARCASCADE_CAMERA_PATH}")
        if HAARCASCADE_CAMERA_PATH and os.path.exists(HAARCASCADE_CAMERA_PATH):
            self.face_cascade = cv2.CascadeClassifier(HAARCASCADE_CAMERA_PATH)
            if self.face_cascade.empty():
                print(f"[!] Critical Error: Failed to load Haar Cascade for face detection from {HAARCASCADE_CAMERA_PATH}, even though file exists.")
                print("    OpenCV might not be able to read/parse the file. Face detection in the camera feed will NOT work.")
                self.face_cascade = None # Ensure it's None if loading failed
                self.recognition_enabled = False
            else:
                print(f"[✓] Haar Cascade for face detection loaded successfully.")
        else:
            print(f"[!] Critical Error: Haar Cascade file path is invalid or file does not exist: '{HAARCASCADE_CAMERA_PATH}'.")
            print("    Face detection in the camera feed will NOT work.")
            self.face_cascade = None # Ensure it's None
            self.recognition_enabled = False


        # --- Initial Model Load (Now self.cap and self.face_cascade are initialized) ---
        self.reload_model_data() # Call the method to load face recognition model data

        self.after_id = None # For managing Tkinter's after calls

        # --- UI Setup ---
        self.mainPanel = tk.LabelFrame(self, bg="white", relief=tk.SUNKEN, bd=1)
        self.leftPanel = tk.LabelFrame(self, bg=BG_COLOR, relief=tk.SUNKEN, bd=1)

        self.columnconfigure(0, weight=2) # Left panel (notifications, controls)
        self.columnconfigure(1, weight=5) # Main panel (camera feed) - give more weight
        self.rowconfigure(0, weight=1) # Only one row, make it expand

        self.leftPanel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.mainPanel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # --- Main Panel Widgets ---
        self.title_video = tk.Label(
            self.mainPanel, bg=BG_COLOR, fg="black",
            text="Camera Sảnh Chính", font=("Arial", 18, "bold"), # Slightly smaller font for balance
            anchor="center", justify="center", bd=0, padx=10, pady=10,
        )
        self.show_camera = tk.Label(self.mainPanel, bg="#333333", bd=0) # Darker bg for camera area

        self.mainPanel.rowconfigure(0, weight=0) # Title row doesn't expand vertically
        self.mainPanel.rowconfigure(1, weight=1) # Camera feed row expands vertically
        self.mainPanel.columnconfigure(0, weight=1) # Single column expands horizontally

        self.title_video.grid(row=0, column=0, sticky="ew", pady=(0,5)) # Use ew for horizontal fill
        self.show_camera.grid(row=1, column=0, sticky="nsew")


        # --- Left Panel Widgets (Notifications & Reload Button) ---
        self.notification_title = tk.Label(
            self.leftPanel, bg=BG_COLOR, fg="black",
            text="Thông báo nhận diện", font=("Arial", 14, "bold"), # Adjusted font
            anchor="w", padx=10 # pady removed from constructor
        )
        self.notification_box = tk.Text(
            self.leftPanel, height=10, bg="white", fg="black", # Increased height
            state="disabled", bd=1, relief=tk.SOLID, padx=5, pady=5, wrap="word",
            font=("Arial", 9)
        )
        
        self.reload_button = tk.Button(
            self.leftPanel,
            text="Tải lại Model Khuôn mặt",
            command=self.reload_model_data_and_notify,
            font=("Arial", 10, "bold"),
            bg="#3498DB", # Calmer Blue
            fg="white",
            relief=tk.RAISED,
            bd=2, padx=10, pady=6, # Increased padding
            activebackground="#2980B9",
            activeforeground="white"
        )

        self.leftPanel.rowconfigure(0, weight=0) # Title
        self.leftPanel.rowconfigure(1, weight=1) # Notification box (allow to expand)
        self.leftPanel.rowconfigure(2, weight=0) # Reload button
        self.leftPanel.columnconfigure(0, weight=1) # Single column

        # Apply specific pady for notification_title in the grid call
        self.notification_title.grid(row=0, column=0, sticky="ew", padx=5, pady=(10, 5)) 
        self.notification_box.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.reload_button.grid(row=2, column=0, sticky="ew", padx=5, pady=10)


        # --- Recognition Logging ---
        self.last_logged_times = {}
        # Ensure 'view' directory exists or change path. If camera.py is in view, this is fine.
        # If timelog.txt should be in the project root or a 'logs' folder:
        # self.timelog_file_path = os.path.join(CAMERA_DIR, "..", "timelog.txt") # Example for root
        self.timelog_file_path = "timelog.txt" # Simpler: place it where script is run from, or in 'view'
        if not os.path.isabs(self.timelog_file_path) and "view" in CAMERA_DIR: # Heuristic
             self.timelog_file_path = os.path.join(CAMERA_DIR, "timelog.txt")

        # Create directory for timelog if it's not in the current dir and path suggests a subdir
        log_dir = os.path.dirname(self.timelog_file_path)
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir, exist_ok=True)
                print(f"[✓] Created directory for timelog: {log_dir}")
            except OSError as e:
                print(f"[!] Error creating directory {log_dir} for timelog: {e}")
        print(f"[*] Timelog will be saved to: {os.path.abspath(self.timelog_file_path)}")


        # --- Start Update Loop ---
        if self.running: # self.running is set based on camera initialization
            self.update_frame()
        else:
            err_msg = "Lỗi: Không thể mở webcam!"
            if self.face_cascade is None:
                err_msg += "\nKhông thể tải Haar Cascade!"
            print(f"[!] Camera not running. UI message: {err_msg.replace('\n', ' ')}")
            # Ensure show_camera is wide enough before setting wraplength
            self.show_camera.update_idletasks() 
            wraplen = self.show_camera.winfo_width() - 20 if self.show_camera.winfo_width() > 40 else 200
            self.show_camera.config(text=err_msg, fg="white", bg="#550000", font=("Arial", 16), wraplength=wraplen)


    def reload_model_data(self):
        """Loads or reloads the face recognition model components."""
        print("\n[*] Attempting to load/reload face recognition model data...")
        # Assume recognition is disabled until all components load successfully
        self.recognition_enabled = False 
        try:
            mean_face, eigvecs, X_projected, labels, _ = load_model(num_components=10) # Unpack 5th if returned
            label_map = build_label_map()

            self.mean_face = mean_face
            self.eigvecs = eigvecs
            self.X_projected = X_projected
            self.labels = labels
            self.label_map = label_map if label_map is not None else {}
            self.recognition_components = (self.mean_face, self.eigvecs, self.X_projected, self.labels)

            model_components_loaded = all(comp is not None for comp in self.recognition_components)
            label_map_loaded = bool(self.label_map)

            if model_components_loaded and label_map_loaded:
                # Now, also check if camera and face_cascade (for detection) are operational
                if self.cap and self.cap.isOpened() and self.face_cascade and not self.face_cascade.empty():
                    self.recognition_enabled = True
                    print("[✓] Face recognition model data reloaded AND prerequisites (camera, cascade) are MET.")
                    # Optionally print shapes if debugging, can be verbose
                    # print(f"    - Mean face shape: {self.mean_face.shape if hasattr(self.mean_face, 'shape') else 'N/A'}")
                    # print(f"    - Eigvecs shape: {self.eigvecs.shape if hasattr(self.eigvecs, 'shape') else 'N/A'}")
                    # print(f"    - X_projected shape: {self.X_projected.shape if hasattr(self.X_projected, 'shape') else 'N/A'}")
                    # print(f"    - Labels count: {len(self.labels) if self.labels is not None else 'N/A'}")
                    # print(f"    - Label map size: {len(self.label_map)}")
                else:
                    print("[!] Warning: Model data loaded, but camera or detection cascade is NOT ready. Recognition remains disabled.")
                    if not (self.cap and self.cap.isOpened()):
                        print("    - Camera is not open.")
                    if not (self.face_cascade and not self.face_cascade.empty()):
                        print("    - Face detection cascade is not loaded.")
            else:
                print("[!] Warning: Face recognition model data (Eigenfaces, labels) could not be fully loaded/reloaded.")
                if not model_components_loaded:
                    print("    - One or more Eigenface components are missing.")
                if not label_map_loaded:
                    print("    - Label map is empty or could not be built.")
                self.recognition_components = (None, None, None, None) # Ensure reset
                self.label_map = {}
        
        except Exception as e:
            # self.recognition_enabled remains False from the top of the try block
            self.recognition_components = (None, None, None, None)
            self.label_map = {}
            print(f"[!] CRITICAL Exception during model data loading/reloading: {e}", exc_info=True) # exc_info for traceback
            print("    Face recognition will be disabled.")

        # This check is now integrated above, but a final status print is good.
        if not self.recognition_enabled:
             print("[!] Note: Overall face recognition is currently DISABLED. Check logs for details.")
        
        print(f"[*] Recognition enabled status after reload attempt: {self.recognition_enabled}\n")


    def reload_model_data_and_notify(self):
        """Wrapper for reload_model_data to add a UI notification."""
        print("[*] Reload button clicked. Reloading model...")
        self.reload_model_data() 
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        if self.recognition_enabled:
            message = f"[{timestamp}] Model đã được tải lại thành công."
            print("[✓] UI Notification: Model reloaded successfully.")
        else:
            message = f"[{timestamp}] Lỗi khi tải lại model. Xem console."
            print("[!] UI Notification: Error reloading model.")
        
        self.notifications.insert(0, message) # Insert at the beginning for newest first
        max_notifications = 15 # Allow more notifications
        if len(self.notifications) > max_notifications:
            self.notifications = self.notifications[:max_notifications]
        self.update_notifications_display()


    def update_notifications_display(self): # Renamed for clarity
        self.notification_box.config(state="normal")
        self.notification_box.delete("1.0", tk.END)
        # No need to reverse self.notifications if always inserting at index 0
        new_text = "\n".join(self.notifications) 
        self.notification_box.insert("1.0", new_text)
        self.notification_box.config(state="disabled")
        self.notification_box.see("1.0") # Scroll to top


    def update_frame(self):
        if not self.running:
            print("[*] Stopping update_frame loop (running is False).")
            self._cleanup_resources()
            return

        # This check should ideally not be needed if self.running is managed correctly
        if self.cap is None or not self.cap.isOpened():
            print("[!] Error: Camera not available in update_frame. Forcing stop.")
            self.running = False
            # Schedule one last call for cleanup, then display error
            if self.after_id: self.show_camera.after_cancel(self.after_id) # Cancel existing
            self.after_id = self.show_camera.after(10, self._handle_camera_failure_in_ui)
            return

        ret, frame = self.cap.read()
        if not ret or frame is None:
            print("[!] Error: Can't receive frame from camera (ret=False or frame is None). Forcing stop.")
            self.running = False
            if self.after_id: self.show_camera.after_cancel(self.after_id)
            self.after_id = self.show_camera.after(10, self._handle_camera_failure_in_ui)
            return
        
        processed_frame = frame.copy() # Work on a copy

        # --- Perform Detection/Recognition ---
        if self.face_cascade and not self.face_cascade.empty():
            gray = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40,40)) # Slightly larger minSize

            if self.recognition_enabled: # Full recognition
                mean_face, eigvecs, X_projected, labels = self.recognition_components
                for (x, y, w, h) in faces:
                    face_resized = preprocess_face_from_frame(gray, (x, y, w, h))
                    if face_resized is not None and face_resized.size > 0 : # Check if preprocessing was successful
                        face_flat = face_resized.flatten()
                        # Ensure mean_face and eigvecs are not None before projecting
                        if mean_face is not None and eigvecs is not None:
                            face_proj = project_face(face_flat, mean_face, eigvecs)
                            if face_proj is not None:
                                name, distance = recognize_face_from_projection(
                                    face_proj, X_projected, labels, self.label_map, threshold=RECOGNITION_THRESHOLD
                                )
                                draw_prediction_on_frame(processed_frame, name, distance, x, y, w, h, threshold=RECOGNITION_THRESHOLD)
                                self.log_recognition(name)
                        else: # Fallback if model components for projection are missing
                            cv2.rectangle(processed_frame, (x,y), (x+w, y+h), (0,255,255), 2) # Yellow for detected, no projection
                            cv2.putText(processed_frame, "Model Error", (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255),2)
            
            elif len(faces)>0: # Detection only (recognition_enabled is False but cascade works)
                for (x, y, w, h) in faces:
                    cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (255, 0, 0), 2) # Blue for detected
                    cv2.putText(processed_frame, "Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        # else: # No face_cascade loaded, do nothing with frame regarding faces

        # --- Display Frame in Tkinter ---
        try:
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)

            label_width = self.show_camera.winfo_width()
            label_height = self.show_camera.winfo_height()

            if label_width > 1 and label_height > 1: 
                img_width, img_height = img.size
                if img_width > 0 and img_height > 0: # Ensure img dimensions are valid
                    aspect_ratio = img_width / img_height
                    
                    new_width = label_width
                    new_height = int(new_width / aspect_ratio)
                    
                    if new_height > label_height:
                        new_height = label_height
                        new_width = int(new_height * aspect_ratio)
                    
                    if new_width > 0 and new_height > 0: 
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            imgtk = ImageTk.PhotoImage(image=img)
            self.show_camera.imgtk = imgtk 
            self.show_camera.config(image=imgtk, text="") 
        except Exception as e:
            print(f"[!] Error updating Tkinter image: {e}")

        if self.running:
            if self.after_id: self.show_camera.after_cancel(self.after_id) 
            self.after_id = self.show_camera.after(20, self.update_frame) 


    def _handle_camera_failure_in_ui(self):
        """Displays a camera failure message in the UI."""
        print("[!] _handle_camera_failure_in_ui called.")
        self.show_camera.config(image=None) 
        err_msg = "Lỗi: Webcam bị ngắt kết nối hoặc không hoạt động."
        if self.face_cascade is None: 
            err_msg += "\n(Cascade dò mặt cũng lỗi)"
        
        self.show_camera.update_idletasks() 
        current_width = self.show_camera.winfo_width()
        wraplen = current_width - 20 if current_width > 40 else 200
        self.show_camera.config(text=err_msg, fg="white", bg="#770000", font=("Arial", 16), wraplength=wraplen)


    def log_recognition(self, name):
        if not name or name in ["Unknown", "Error", "Placeholder"]:
            return

        now = time.time()
        last_time = self.last_logged_times.get(name, 0)
        if now - last_time >= 10: 
            timestamp_dt = datetime.now()
            timestamp_str_log = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"Nhận diện: {name} vào lúc [{timestamp_str_log}]\n"
            try:
                with open(self.timelog_file_path, "a", encoding="utf-8") as f:
                    f.write(log_entry)
            except Exception as e:
                print(f"[!] Error writing to {self.timelog_file_path}: {e}")

            timestamp_str_ui = timestamp_dt.strftime('%H:%M:%S')
            notification_text = f"🎯 {name} @ {timestamp_str_ui}" 
            
            self.notifications.insert(0, notification_text) 
            max_notifications = 15
            if len(self.notifications) > max_notifications:
                 self.notifications = self.notifications[:max_notifications]
            self.update_notifications_display()
            self.last_logged_times[name] = now


    def _cleanup_resources(self):
        """Internal method to release camera."""
        print("[*] _cleanup_resources called.")
        if hasattr(self, 'cap') and self.cap is not None:
            if self.cap.isOpened():
                print("[*] Releasing camera resource...")
                self.cap.release()
                print("[✓] Camera released.")
            self.cap = None
        print("[✓] OpenCV resource cleanup (camera release) attempted.")


    def stop_camera(self):
        """Public method to signal the camera loop to stop and clean up."""
        print("[*] stop_camera() called. Setting running to False.")
        self.running = False 
        
        if self.after_id is not None:
            try:
                if hasattr(self, 'show_camera') and self.show_camera.winfo_exists():
                    self.show_camera.after_cancel(self.after_id)
                    print("[✓] Cancelled pending Tkinter 'after' call in stop_camera.")
                else:
                    print("[!] Could not cancel 'after' call: show_camera widget does not exist or already destroyed.")
            except tk.TclError as e:
                print(f"[!] Error cancelling 'after' call in stop_camera: {e}")
            self.after_id = None
        
        self._cleanup_resources()
        print("[*] stop_camera() finished.")


    def __del__(self):
        """Destructor: attempts to clean up resources."""
        print(f"[*] Camera object __del__ for {id(self)} called.")
        self.running = False 
        if hasattr(self, 'after_id') and self.after_id is not None:
            if hasattr(self, 'show_camera') and isinstance(self.show_camera, tk.Widget) and self.show_camera.winfo_exists():
                try:
                    self.show_camera.after_cancel(self.after_id)
                    print("[✓] Cancelled pending Tkinter 'after' call in __del__.")
                except tk.TclError:
                    print("[!] Warning: Could not cancel 'after' call in __del__ (widget/Tcl interpreter might be gone).")
            self.after_id = None
        self._cleanup_resources()
        print(f"[*] Camera object __del__ for {id(self)} finished.")
