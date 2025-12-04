import cv2
import threading
from voice.speech import speak

class VisionMode:
    def __init__(self):
        self.running = False
        self.last_seen_objects = []
        self.cap = None

    def start(self):
        print("[DEBUG] Starting VisionMode...")
        if self.running:
            speak("Vision is already active.")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_vision, daemon=True)
        self.thread.start()
        speak("Vision mode activated. I can now see through the camera.")
        print("🧠 Vision Mode: Say 'what do you see' or 'stop vision'.")

    def stop(self):
        print("[DEBUG] Stopping VisionMode...")
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        speak("Vision mode stopped.")
        print("🛑 Vision stopped.")

    def _run_vision(self):
        print("[DEBUG] Vision thread running...")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            speak("Unable to access the camera.")
            print("[ERROR] Cannot open camera.")
            self.running = False
            return

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            current_objects = []

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                current_objects.append("human face")

            self.last_seen_objects = list(set(current_objects))
            cv2.imshow("JARVIS Vision", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def describe_view(self):
        print("[DEBUG] Describing current view...")
        if not self.last_seen_objects:
            speak("I don't see anything right now.")
        else:
            speak("I can see " + ", ".join(self.last_seen_objects))
