import cv2
import threading
import time
from torchvision import transforms

class ThreadedCameraStream:
    """Handles individual camera streams in a separate thread to prevent blocking the main loop."""
    def __init__(self, src):
        self.stream = cv2.VideoCapture(src)
        self.ret, self.frame = self.stream.read()
        self.stopped = False
        self.lock = threading.Lock()
        
        # Start background thread to read frames
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while not self.stopped:
            if not self.stream.isOpened():
                break
            ret, frame = self.stream.read()
            if ret:
                with self.lock:
                    self.ret, self.frame = ret, frame
            else:
                time.sleep(0.01)

    def read(self):
        with self.lock:
            return self.ret, self.frame.copy() if self.frame is not None else None

    def release(self):
        self.stopped = True
        self.thread.join()
        self.stream.release()


# --- Surveillance Network Configuration ---
# You can mix local USB cameras (indices) and network streams (RTSP/HTTP URLs)
CAMERA_SOURCES = {
    "primary_nav": 0,                      # Local robot camera
    "surveillance_zone_a": "rtsp://192.168.1.50:554/stream1",  # Example IP camera
    # "surveillance_zone_b": "http://192.168.1.51/video",      # Example HTTP stream
}

# Preprocessing pipeline
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def initialize_surveillance_network():
    streams = {}
    for name, src in CAMERA_SOURCES.items():
        print(f"Connecting to camera [{name}] at source {src}...")
        streams[name] = ThreadedCameraStream(src)
    return streams

def capture_all_feeds(streams):
    """Pulls the latest frame from all active cameras simultaneously."""
    processed_frames = {}
    for name, stream in streams.items():
        ret, frame = stream.read()
        if ret and frame is not None:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_frames[name] = transform(frame_rgb).unsqueeze(0) # Shape: (1, 3, 224, 224)
        else:
            processed_frames[name] = None
    return processed_frames
