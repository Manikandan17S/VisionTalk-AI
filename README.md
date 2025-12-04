# VisionTalk AI

VisionTalk AI — an offline voice & vision assistant built with Ollama, PyQt5, OpenCV and Python.
It supports offline reasoning (Ollama Phi-3 Mini), real-time object/face detection, voice input (SpeechRecognition) and offline TTS (pyttsx3).

    ## Features
    - Offline LLM reasoning (Ollama)
    - Real-time webcam face/object detection
    - Voice input (microphone) and offline TTS responses
    - Holographic-style UI (PyQt5)
    - Modular architecture for easy extension

    ## Requirements
    - Python 3.10+
    - Ollama installed and a local model (Phi-3 Mini)
    - System deps: portaudio (for PyAudio) — see `docs/INSTALL.md`
    - Install Python packages:
    ```bash
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt

How to run

Install Ollama and pull model:

    # Example (run locally):
    ollama pull phi-3-mini

Start the app:
    python src/main.py
