import random
import string
import tkinter as tk

import cv2
import numpy
from numpy import printoptions, random
from numpy.__config__ import show
from PIL import Image, ImageTk
from recognize_faces import load_model, preprocess_face_from_frame, project_face, recognize_face_from_projection, build_label_map
from datetime import datetime
import time

color1 = "#e3e3e3"
video_path1 = "color.mp4"
video_path2 = "720p.mp4"
video_path3 = "1080p.mp4"

alert_notifications = [
    "🔔 Motion detected!",
    "✅ Camera is online",
    "⚠️  Low light warning",
    "🆕 New face detected",
    "🔄 Video feed refreshed",
]


class Camera(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        # panel
        self.mainPanel = tk.LabelFrame(self, bg="white")
        self.leftPanel = tk.LabelFrame(self, bg=color1)
        self.notifications = []

        # configure weights
        self.columnconfigure(0, weight=2)  # Left panel 2/8
        self.columnconfigure(1, weight=6)  # Main panel 6/8
        self.rowconfigure(0, weight=1)  

        # place LabelFrames
        self.leftPanel.grid(row=0, column=0, sticky="nsew")
        self.mainPanel.grid(row=0, column=1, sticky="nsew")

        # ========================================================
        self.title_video = tk.Label(
            self.mainPanel,
            bg=color1,
            fg="black",
            text="Motel Main Camera View",
            font=("Arial", 20, "bold"),
            anchor="center",
            justify="center",
            bd=0,
            padx=10,
            pady=10,
        )
        self.show_camera = tk.Label(self.mainPanel, bg=color1, bd=0)
        self.notification_box = tk.Text(
            self.leftPanel,
            height=5,
            width=10,
            bg=color1,
            fg="black",
            state="disabled",
            bd=0,
            padx=10,
            pady=10,
        )

        # main weight
        self.mainPanel.rowconfigure(0, weight=2)
        self.mainPanel.rowconfigure(1, weight=80)
        self.mainPanel.columnconfigure(0, weight=1)

        # left panel
        self.notification_box.pack(expand=True, fill="both")
        self.auto_generate_notifications()

        # label
        self.title_video.grid(row=0, column=0, sticky="nsew")
        self.show_camera.grid(row=1, column=0, sticky="")

        # add camera
        self.show_camera = tk.Label(
            self.mainPanel, bg=color1, height=1280, width=720
        )
        self.show_camera.grid(row=1, column=0, sticky="nsew")
        # mở cam và thêm phần nhận diện khuôn mặt + ghi time
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.mean_face, self.eigvecs, self.X_projected, self.labels = load_model(num_components=10)
        self.label_map = build_label_map("dataset")
        self.last_logged_times = {}
        self.update_frame()

    def get_notification(self, strings):
        noti = random.choice(strings)
        return tk.Label(self, text=noti)

    def get_random_string(self):
        return random.choice(alert_notifications)

    def auto_generate_notifications(self):
        new_notification = self.get_random_string()

        # add to notification list
        self.notifications.append(new_notification)

        # refresh displayed notifications
        self.update_notifications()

        # show notifications
        self.after(12000, self.remove_oldest_notifications)
        self.after(2500, self.auto_generate_notifications)

    def remove_oldest_notifications(self):
        if self.notifications:
            self.notifications.pop(0)  # remove first (oldest) item
            self.update_notifications()

    def update_notifications(self):
        self.notification_box.config(state="normal")
        self.notification_box.delete("1.0", tk.END)  # Clear all text

        # insert new notifications first (newest at the top)
        new_text = "\n".join(self.notifications[::-1])  # Reverse the list
        self.notification_box.insert("1.0", new_text)  # Insert all at the top
        self.notification_box.config(state="disabled")

    # temp funtion show video/camera ==================================================
    def update_frame(self):
        """Fetch frame from VideoStream and update Label"""
        ret, frame = self.cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_flat = preprocess_face_from_frame(gray, (x, y, w, h))
            face_proj = project_face(face_flat, self.mean_face, self.eigvecs)
            name, distance = recognize_face_from_projection(face_proj, self.X_projected, self.labels, self.label_map, threshold=1500)
            self.log_recognition(name)
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.putText(frame, f"{name} ({distance:.2f})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((960, 720))  
        imgtk = ImageTk.PhotoImage(image=img)

        self.show_camera.imgtk = imgtk
        self.show_camera.config(image=imgtk)
        self.show_camera.after(10, self.update_frame)
    def log_recognition(self, name):
        now = time.time()
        last_time = self.last_logged_times.get(name, 0)
        if now - last_time >= 10:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"Nhận diện: {name} vào lúc [{timestamp}]\n"
            with open("timelog.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)

            # hiện trên noti box
            self.notifications.append(f"🎯 Nhận diện: {name} vào lúc [{timestamp}] ")
            self.update_notifications()

            self.last_logged_times[name] = now
    def __del__(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()