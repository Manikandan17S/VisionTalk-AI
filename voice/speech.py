import threading
import queue
import pyttsx3
import time

class SpeechEngine:
    def __init__(self, rate=175, volume=1.0, voice_index=0):
        self._queue = queue.Queue()
        self._engine = None
        self._rate = rate
        self._volume = volume
        self._voice_index = voice_index
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._started = False
        self._lock = threading.Lock()

    def start(self):
        if not self._started:
            self._thread.start()
            self._started = True
class SpeechEngine:
    def __init__(self, rate=175, volume=1.0, voice_index=0):
        self._queue = queue.Queue()
        self._engine = None
        self._rate = rate
        self._volume = volume
        self._voice_index = voice_index
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._started = False
        self._lock = threading.Lock()

    def start(self):
        if not self._started:
            self._thread.start()
            self._started = True

    def _init_engine(self):
        if self._engine is None:
            try:
                self._engine = pyttsx3.init('sapi5')
            except Exception as e:
                print("[SpeechEngine] Warning initializing sapi5:", e)
            self._engine = pyttsx3.init()  # fallback

        try:
            self._engine.setProperty('rate', self._rate)
            self._engine.setProperty('volume', self._volume)

            voices = self._engine.getProperty('voices')
            if voices:
                # ✅ Use a known English voice (avoid index issues)
                for v in voices:
                    if "Zira" in v.name or "David" in v.name:
                        self._engine.setProperty('voice', v.id)
                        print(f"[SpeechEngine] Using voice: {v.name}")
                        break
                else:
                    self._engine.setProperty('voice', voices[0].id)
                    print(f"[SpeechEngine] Using default voice: {voices[0].name}")
        except Exception as e:
            print(f"[SpeechEngine] Error setting voice properties: {e}")

    def _run(self):
        while True:
            text = self._queue.get()
            if text is None:
                break

            try:
                # create a fresh engine inside this thread each time
                engine = pyttsx3.init('sapi5')
                engine.setProperty('rate', self._rate)
                engine.setProperty('volume', self._volume)

                voices = engine.getProperty('voices')
                if voices:
                    for v in voices:
                        if "David" in v.name or "Zira" in v.name:
                            engine.setProperty('voice', v.id)
                            break
                    else:
                        engine.setProperty('voice', voices[0].id)

                print("JARVIS (speaking):", text)
                engine.say(text)
                engine.runAndWait()
                engine.stop()
                del engine

            except Exception as e:
                print(f"[SpeechEngine] Error during speak: {e}")

            finally:
                try:
                    self._queue.task_done()
                except Exception:
                    pass

    def speak_async(self, text):
        """Queue text for speaking and return immediately."""
        if not text:
            return
        self.start()
        # Put trimmed text in queue
        self._queue.put(str(text))
        print("[SpeechEngine] Queued speech.")

    def stop(self):
        """Immediately stop current speech and clear queued items."""
        # stop the engine speaking right now
        with self._lock:
            if self._engine:
                try:
                    self._engine.stop()
                    print("[SpeechEngine] Engine.stop() called.")
                except Exception as e:
                    print(f"[SpeechEngine] Error calling stop(): {e}")

            # clear pending queue items (non-blocking)
            try:
                while True:
                    item = self._queue.get_nowait()
                    # mark removed
                    try:
                        self._queue.task_done()
                    except Exception:
                        pass
            except Exception:
                # queue empty
                pass

    def shutdown(self):
        """Cleanly shutdown speaking thread (optional)."""
        try:
            self._queue.put(None)
        except Exception:
            pass

# Singleton instance for app-wide use
speech_engine = SpeechEngine()

# Convenience wrappers for import compatibility
def speak(text):
    speech_engine.speak_async(text)

def stop():
    speech_engine.stop()


    def _run(self):
        while True:
            text = self._queue.get()  # blocks until text available
            if text is None:
                # sentinel to stop thread
                break

            # initialize engine on this thread
            self._init_engine()

            try:
                print("JARVIS (speaking):", text)
                # engine.say and runAndWait are blocking but run in this thread only
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception as e:
                print(f"[SpeechEngine] Error during speak: {e}")
            finally:
                # mark done
                try:
                    self._queue.task_done()
                except Exception:
                    pass

    def speak_async(self, text):
        """Queue text for speaking and return immediately."""
        if not text:
            return
        self.start()
        # Put trimmed text in queue
        self._queue.put(str(text))
        print("[SpeechEngine] Queued speech.")

    def stop(self):
        """Immediately stop current speech and clear queued items."""
        # stop the engine speaking right now
        with self._lock:
            if self._engine:
                try:
                    self._engine.stop()
                    print("[SpeechEngine] Engine.stop() called.")
                except Exception as e:
                    print(f"[SpeechEngine] Error calling stop(): {e}")

            # clear pending queue items (non-blocking)
            try:
                while True:
                    item = self._queue.get_nowait()
                    # mark removed
                    try:
                        self._queue.task_done()
                    except Exception:
                        pass
            except Exception:
                # queue empty
                pass

    def shutdown(self):
        """Cleanly shutdown speaking thread (optional)."""
        try:
            self._queue.put(None)
        except Exception:
            pass

# Singleton instance for app-wide use
speech_engine = SpeechEngine()

# Convenience wrappers for import compatibility
def speak(text):
    speech_engine.speak_async(text)

def stop():
    speech_engine.stop()
