import cv2
from PIL import Image, ImageTk

class VideoStream:
    def __init__(self, video_source):
        """Initialize video source (default is webcam)"""
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)

        if not self.vid.isOpened():
            raise Exception("Error: Unable to open video source")

    def get_frame(self):
        """Capture frame, convert it, and return it in Tkinter-compatible format"""
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            img = Image.fromarray(frame)  # Convert to PIL image
            return ImageTk.PhotoImage(image=img)  # Convert to Tkinter-compatible image
        return None  # If no frame is captured, return None

    def release(self):
        """Release the video capture"""
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()
