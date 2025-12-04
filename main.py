import socket
import sys
import threading
import time as time_module
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QApplication
from voice.speech import speech_engine, speak, stop as stop_speaking
from voice.recognition import listen
from ai.brain import ai_respond
from vision.face_detect import VisionMode
from gui.advanced_interface import JarvisUI
from utils.system_control import SystemControl

# Initialize system control
system_control = SystemControl()

def has_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False

class JarvisWorker(QObject):
    """Worker thread for JARVIS logic"""
    status_changed = pyqtSignal(str)
    text_updated = pyqtSignal(str)
    response_updated = pyqtSignal(str)
    history_added = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        """Main JARVIS loop"""
        speak("JARVIS online. Ready to assist.")   # non-blocking now
        self.status_changed.emit("Ready")

        while self.running:
            try:
                self.status_changed.emit("Listening")
                command = listen()

                self.text_updated.emit(command)

                if command == "none":
                    self.status_changed.emit("Standby")
                    continue

                # If user explicitly says stop / cancel / interrupt, stop current speech.
                if any(w in command for w in ["stop", "cancel", "interrupt"]):
                    print("[Main] Stop command detected — stopping speech.")
                    speech_engine.stop()
                    self.history_added.emit(command)
                    self.status_changed.emit("Standby")
                    continue

                self.history_added.emit(command)

                if any(word in command for word in ["exit", "quit", "bye"]):
                     self.status_changed.emit("Shutting down")
                     speak("Goodbye!")
                     time_module.sleep(1)
                     speech_engine.stop()
                     self.status_changed.emit("Restarting JARVIS...")
                     speak("Restarting systems.")
                     continue

                # ... system_control block unchanged, but replace speak(...) calls with speak(...)
                if any(word in command for word in ["open", "search", "google", "youtube", 
                                                     "shutdown", "restart", "lock", "volume",
                                                     "battery", "system info", "screenshot",
                                                     "files", "list"]):
                    self.status_changed.emit("Processing")
                    system_response = system_control.execute_command(command)
                    self.response_updated.emit(system_response)
                    self.status_changed.emit("Responding")
                    speak(system_response)  # non-blocking
                    self.status_changed.emit("Standby")
                    continue

                if any(word in command for word in ["start vision", "detect face", "camera mode", "open vision"]):
                     print("[DEBUG] Vision trigger detected:", command)
                     self.status_changed.emit("Activating Vision Mode")
                     from vision.face_detect import VisionMode
                     vision = VisionMode()
                     vision.start()
                     self.status_changed.emit("Vision Mode ended.")
                     continue
                
                if "camera mode" in command or "vision mode" in command:
                     self.status_changed.emit("Vision")
                     self.vision = VisionMode()
                     self.vision.start()
                     continue
                
                if "what do you see" in command and hasattr(self, "vision"):
                     self.vision.describe_view()
                     continue
                if "stop vision" in command and hasattr(self, "vision"):
                     self.vision.stop()
                     continue

                # ========== AI RESPONSE ==========
                self.status_changed.emit("Processing")
                response = ai_respond(command)
                self.response_updated.emit(response)
                self.status_changed.emit("Responding")

                if response:
                    speak(response)   # non-blocking now

                self.status_changed.emit("Standby")

            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                self.response_updated.emit(f"Error: {str(e)}")
                self.status_changed.emit("Error")
    

def main():
    app = QApplication(sys.argv)
    
    gui_window = JarvisUI()
    gui_window.show()
    
    worker = JarvisWorker()
    
    worker.status_changed.connect(gui_window.update_status)
    worker.text_updated.connect(gui_window.update_text)
    worker.response_updated.connect(gui_window.update_response)
    worker.history_added.connect(gui_window.add_to_history)
    
    worker_thread = threading.Thread(target=worker.run, daemon=True)
    worker_thread.start()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
