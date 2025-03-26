import random
import string
import tkinter as tk
import cv2
import numpy
from numpy import printoptions, random
from numpy.__config__ import show
from PIL import Image, ImageTk
from video_stream import VideoStream

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
        mainPanel.rowconfigure(1, weight=1)
        mainPanel.columnconfigure(0, weight=1)
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
        """Fetch frame from VideoStream and update Label"""
        frame = self.video_stream.get_frame()
        if frame:
            self.show_camera.imgtk = frame
            self.show_camera.config(image=frame)

        # update every 10ms
        self.show_camera.after(10, self.update_frame)

    def __del__(self):
        """Giải phóng webcam khi đóng ứng dụng"""
        self.cap.release()
        cv2.destroyAllWindows()