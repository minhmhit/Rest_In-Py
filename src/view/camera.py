import tkinter as tk
import cv2
from PIL import Image, ImageTk
import os
color1 = "#deffff"
class Camera(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        # kết nối đến model nhận diện khuôn mặt
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_recognizer.read("trainer.yml")  # load model đã train
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # load danh sách tên từ dataset
        self.label_map = {i: name for i, name in enumerate(os.listdir("dataset"))}
        # giao diện chính
        mainPanel = tk.LabelFrame(self, bg='white')
        leftPanel = tk.LabelFrame(self, bg=color1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)
        self.rowconfigure(0, weight=1)
        leftPanel.grid(row=0, column=0, sticky="nsew")
        mainPanel.grid(row=0, column=1, sticky="nsew")
        # title
        title_video = tk.Label(mainPanel, bg=color1, text="SHOW CAMERA", 
                               font=("Arial", 20, "bold"), anchor="center", justify="center")
        title_video.grid(row=0, column=0, sticky="nsew")
        # label hiển thị camera 
        self.show_camera = tk.Label(mainPanel, bg=color1, height=480, width=640)
        self.show_camera.grid(row=1, column=0, sticky="nsew")
        mainPanel.rowconfigure(1, weight=1)
        mainPanel.columnconfigure(0, weight=1)
        self.cap = cv2.VideoCapture(0)
        self.update_frame()
    def update_frame(self):
        """Lấy frame từ webcam và cập nhật giao diện"""
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                label, confidence = self.face_recognizer.predict(face_img)
                if confidence < 100:
                    name = self.label_map.get(label, "Unknown")
                    confidence_text = f"{100 - confidence:.2f}%"
                else:
                    name = "Unknown"
                    confidence_text = ""
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"{name} {confidence_text}", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            # chuyển đổi frame opencv sang định dạng tkinter
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.show_camera.imgtk = imgtk
            self.show_camera.config(image=imgtk)
        self.after(10, self.update_frame)

    def __del__(self):
        """Giải phóng webcam khi đóng ứng dụng"""
        self.cap.release()
        cv2.destroyAllWindows()