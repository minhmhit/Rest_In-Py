import random
import string
import tkinter as tk
import cv2
import numpy
from numpy import printoptions, random
from numpy.__config__ import show
from PIL import Image, ImageTk
from video_stream import VideoStream
import datetime
import os

color1 = "#deffff"
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
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("trainer.yml")
        self.names = self.load_names_from_dataset()
        self.last_log_time = datetime.datetime.now()
        # panel
        self.mainPanel = tk.LabelFrame(self, bg="white")
        self.leftPanel = tk.LabelFrame(self, bg=color1)
        self.notifications = []

        # configure weights
        self.columnconfigure(0, weight=2)  # Left panel 2/8
        self.columnconfigure(1, weight=6)  # Main panel 6/8
        self.rowconfigure(0, weight=1)  # Ensure row expands

        # place LabelFrames
        self.leftPanel.grid(row=0, column=0, sticky="nsew")
        self.mainPanel.grid(row=0, column=1, sticky="nsew")

        # ========================================================
        self.title_video = tk.Label(
            self.mainPanel,
            bg="#d4ffff",
            fg="#6f74ff",
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
        self.mainPanel.rowconfigure(1, weight=1)
        self.mainPanel.columnconfigure(0, weight=1)
        self.cap = cv2.VideoCapture(0)
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
"""Hiển thị video từ camera"""
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                if confidence < 50:
                    name = f"User {id}"
                    self.log_face_detection(name)
                else:
                    name = "Unknown"
                self.log_face_detection(name)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = ImageTk.PhotoImage(frame)

            self.show_camera.imgtk = frame
            self.show_camera.config(image=frame)

        self.show_camera.after(10, self.update_frame)

    def log_face_detection(self, name):
        """Ghi nhận thời gian khi phát hiện khuôn mặt (chỉ ghi mỗi 10 giây)"""
        current_time = datetime.datetime.now()
        if (current_time - self.last_log_time).total_seconds() >= 10:
            self.last_log_time = current_time  # cập nhật thời gian ghi log lần cuối
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"📷 {name} phát hiện lúc: {timestamp}"  # ghi tên vào log
            self.notifications.append(log_entry)
            self.update_notifications()
            #print(f"✅ Ghi log: {log_entry}")

    def load_names_from_dataset(self, dataset_path="dataset"):
        names = {}
        if os.path.exists(dataset_path):
            for folder_name in os.listdir(dataset_path):  # duyệt qua từng thư mục con
                names[folder_name] = folder_name
        return names
    def __del__(self):
        """Giải phóng webcam khi đóng ứng dụng"""
        self.cap.release()
        cv2.destroyAllWindows()