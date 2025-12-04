import subprocess
import os
import webbrowser
import pyautogui
import platform
from pathlib import Path
import psutil

class SystemControl:
    """Full PC System Control for JARVIS (Offline AI Assistant)"""

    def __init__(self):
        self.system = platform.system()
        self.home_dir = str(Path.home())

    # ==================== OPEN APPLICATIONS ====================
    def open_app(self, app_name):
        """Open any app (auto-detect installation path)"""
        app_name = app_name.lower().strip()

        # 🔍 Known app paths / URIs
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "cmd": "cmd.exe",
            "terminal": "cmd.exe",
            "explorer": "explorer.exe",
            "chrome": [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                "D:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            ],
            "firefox": [
                "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
            ],
            "vlc": [
                "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
                "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
            ],
            "whatsapp": [
                f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
                f"D:\\Users\\{os.getlogin()}\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
            ],
            "camera": "microsoft.windows.camera:",
            "settings": "ms-settings:",
            "control panel": "control",
            "this pc": "explorer",
            "system info": "msinfo32"
        }

        try:
            path = apps.get(app_name)

            if not path:
                return f"App '{app_name}' not found in list."

            # 📁 If multiple paths, check which exists
            if isinstance(path, list):
                for p in path:
                    if os.path.exists(p):
                        subprocess.Popen(p)
                        return f"Opening {app_name}..."
                return f"App {app_name} not found on this system."
            
            # 🪟 Handle Windows URIs (like ms-settings)
            if path.startswith("microsoft.") or path.startswith("ms-"):
                os.system(f"start {path}")
            else:
                subprocess.Popen(path)

            return f"Opening {app_name}..."
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"

    # ==================== CLOSE APPLICATIONS ====================
    def close_app(self, app_name):
        """Close running application"""
        app_name = app_name.lower().strip()
        exe_name = app_name + ".exe"

        # 🔧 Known process names
        process_map = {
            "chrome": "chrome.exe",
            "notepad": "notepad.exe",
            "calculator": "calculator.exe",
            "paint": "mspaint.exe",
            "vlc": "vlc.exe",
            "cmd": "cmd.exe",
            "whatsapp": "whatsapp.exe",
            "explorer": "explorer.exe"
        }

        exe = process_map.get(app_name, exe_name)
        try:
            os.system(f"taskkill /IM {exe} /F")
            return f"Closed {app_name}"
        except Exception as e:
            return f"Error closing {app_name}: {str(e)}"

    # ==================== SYSTEM INFO ====================
    def get_system_info(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            return f"CPU: {cpu}%, RAM: {ram}%, Disk: {disk}%"
        except Exception as e:
            return f"Error: {str(e)}"

    # ==================== SHUTDOWN / RESTART / LOCK ====================
    def shutdown_pc(self):
        os.system("shutdown /s /t 5")
        return "Shutting down in 5 seconds..."

    def restart_pc(self):
        os.system("shutdown /r /t 5")
        return "Restarting in 5 seconds..."

    def lock_pc(self):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "PC locked."

    # ==================== SCREENSHOT ====================
    def take_screenshot(self):
        try:
            save_path = os.path.join(self.home_dir, "Desktop", "screenshot.png")
            pyautogui.screenshot(save_path)
            return f"Screenshot saved at {save_path}"
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    # ==================== COMMAND ROUTER ====================
    def execute_command(self, command):
        """Route voice command to function"""
        command = command.lower().strip()

        # ----- OPEN APPS -----
        if any(word in command for word in ["open", "launch", "start"]):
            app = (
                command.replace("open", "")
                .replace("launch", "")
                .replace("start", "")
                .strip()
            )
            return self.open_app(app)

        # ----- CLOSE APPS -----
        elif any(word in command for word in ["close", "exit", "terminate", "stop"]):
            app = (
                command.replace("close", "")
                .replace("exit", "")
                .replace("terminate", "")
                .replace("stop", "")
                .strip()
            )
            if not app:
                return "Please specify which app to close."
            return self.close_app(app)

        # ----- SYSTEM OPERATIONS -----
        elif "system info" in command:
            return self.get_system_info()
        elif "shutdown" in command:
            return self.shutdown_pc()
        elif "restart" in command:
            return self.restart_pc()
        elif "lock" in command:
            return self.lock_pc()
        elif "screenshot" in command:
            return self.take_screenshot()

        else:
            return "Command not recognized."
