import tkinter as tk

from video_stream import VideoStream
import cv2
from PIL import Image, ImageTk

color1 = "#deffff"
video_path = "video.mp4"

class Camera(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F5F5F5")
        mainPanel = tk.LabelFrame(self,bg='white')
        leftPanel = tk.LabelFrame(self,bg=color1)
        # rightPanel = tk.LabelFrame(self,bg='#8fffff')

        # configure grid weights 
        self.columnconfigure(0, weight=2)  # Left panel 1/5
        self.columnconfigure(1, weight=6)  # Main panel 3/5
        # self.columnconfigure(2, weight=1)  # Right panel 1/5
        self.rowconfigure(0, weight=1)  # Ensure row expands

        # place LabelFrames 
        leftPanel.grid(row=0, column=0, sticky="nsew")
        mainPanel.grid(row=0, column=1, sticky="nsew")
        # rightPanel.grid(row=0, column=2, sticky="nsew")

        #========================================================
        title_video = tk.Label(mainPanel,bg=color1,text="SHOW CAMERA", font=("Arial", 20,"bold"), anchor="center", justify="center")
        show_camera = tk.Label(mainPanel,bg=color1)

        # main weight
        mainPanel.rowconfigure(0,weight=2)
        mainPanel.rowconfigure(1,weight=80)
        mainPanel.columnconfigure(0,weight=1)

        # place Label
        title_video.grid(row=0,column=0,sticky="nsew")
        show_camera.grid(row=1,column=0,sticky="nsew")

        # add camera
        self.show_camera = tk.Label(mainPanel, bg=color1)
        self.show_camera.grid(row=1, column=0, sticky="nsew")
        self.video_stream = VideoStream(video_source=video_path)
        self.update_frame()


    # temp funtion
    def update_frame(self):
        """Fetch frame from VideoStream and update Label"""
        frame = self.video_stream.get_frame()
        if frame:
            self.show_camera.imgtk = frame
            self.show_camera.config(image=frame)

        # Update every 10ms
        self.show_camera.after(10, self.update_frame)

    def __del__(self):
        """Ensure the video stream is released properly"""
        self.video_stream.release()
