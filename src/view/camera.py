import tkinter as tk
import random
import string

from numpy import printoptions, random
import numpy
from numpy.__config__ import show

from video_stream import VideoStream
import cv2
from PIL import Image, ImageTk

color1 = "#deffff"
video_path1 = "color.mp4"
video_path2 = "720p.mp4"
video_path3 = "1080p.mp4"

class Camera(tk.Frame):
    def get_new_label(self,panel,message):
        return tk.Label(panel,bg="green",text=message)

    def remove_notification(self):
        if self.show_log in self.notification:
            self.show_log.destroy()
            self.notification.remove(self.show_log)

    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        self.mainPanel = tk.LabelFrame(self,bg='white')
        self.leftPanel = tk.LabelFrame(self,bg=color1)
        self.notification = [
            tk.Label(self.leftPanel,bg="blue",text=self.get_random_string()),
            tk.Label(self.leftPanel,bg="blue",text=self.get_random_string()),
            tk.Label(self.leftPanel,bg="blue",text=self.get_random_string()),
        ] # panel list
        # rightPanel = tk.LabelFrame(self,bg='#8fffff')

        # configure grid weights 
        self.columnconfigure(0, weight=2)  # Left panel 1/5
        self.columnconfigure(1, weight=6)  # Main panel 3/5
        # self.columnconfigure(2, weight=1)  # Right panel 1/5
        self.rowconfigure(0, weight=1)  # Ensure row expands

        # place LabelFrames 
        self.leftPanel.grid(row=0, column=0, sticky="nsew")
        self.mainPanel.grid(row=0, column=1, sticky="nsew")
        # rightPanel.grid(row=0, column=2, sticky="nsew")

        # ========================================================
        self.title_video = tk.Label(self.mainPanel,bg=color1,text="SHOW CAMERA", font=("Arial", 20,"bold"), anchor="center", justify="center")
        self.show_camera = tk.Label(self.mainPanel,bg=color1)
        self.show_log = tk.Label(self.leftPanel,bg="blue",text=self.get_random_string())

        # main weight
        self.mainPanel.rowconfigure(0,weight=2)
        self.mainPanel.rowconfigure(1,weight=80)
        self.mainPanel.columnconfigure(0,weight=1)

        # left panel
        self.auto_generate_notifications()

        # left panel weight
        self.show_log.pack(fill="x",pady=2)

        #  Label
        self.title_video.grid(row=0,column=0,sticky="nsew")
        self.show_camera.grid(row=1,column=0,sticky="")

        # add camera
        # self.show_camera = tk.Label(mainPanel, bg=color1,height=1280,width=720)
        # self.show_camera.grid(row=1, column=0, sticky="nsew")
        # self.video_stream = VideoStream(video_source=video_path3)
        # self.update_frame()


    def get_random_string(self):
        strings = ["red","green","purple"]
        return random.choice(strings)

    def get_notification(self,strings):
        noti = random.choice(strings)
        return tk.Label(self,text=noti)

    def auto_generate_notifications(self):
        self.get_random_string()
        self.notification.append(self.get_new_label(self,self.get_random_string()))
        self.after(200, self.auto_generate_notifications)
        return self.auto_generate_notifications

    # # temp funtion
    # def update_frame(self):
    #     """Fetch frame from VideoStream and update Label"""
    #     frame = self.video_stream.get_frame()
    #     if frame:
    #         self.show_camera.imgtk = frame
    #         self.show_camera.config(image=frame)
    #
    #     # Update every 10ms
    #     self.show_camera.after(10, self.update_frame)
    #
    # def __del__(self):
    #     """Ensure the video stream is released properly"""
    #     self.video_stream.release()

    

