import speech_recognition as sr

def listen():
    """
    Listen for voice input with better accuracy and longer timeout
    """
    recognizer = sr.Recognizer()
    
    # ========== IMPORTANT SETTINGS FOR BETTER ACCURACY ==========
    recognizer.energy_threshold = 300  
    recognizer.dynamic_energy_threshold = True 
    recognizer.pause_threshold = 1.5  
    recognizer.phrase_threshold = 0.3 
    recognizer.non_speaking_duration = 0.8  
    
    with sr.Microphone() as source:
        print("🎤 Listening... (Speak now)")
        
      
        print("🔇 Adjusting for background noise... (wait 1 second)")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = recognizer.listen(
                source, 
                timeout=5, 
                phrase_time_limit=15 
            )
            
            print("🧠 Recognizing...")
            
            # Use Google Speech Recognition (best accuracy)
            text = recognizer.recognize_google(
                audio,
                language="en-IN"  
            )
            
            print(f"✅ You: {text}")
            return text.lower()
        
        except sr.WaitTimeoutError:
            print("⏰ No speech detected (timeout)")
            return "none"
        
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            return "none"
        
        except sr.RequestError as e:
            print(f"❌ Recognition error: {e}")
            return "none"
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return "none"


def listen_with_wake_word(wake_word="jarvis"):
    """
    Listen for wake word first, then listen for command
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print(f"💤 Waiting for wake word '{wake_word}'...")
        
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # Listen for wake word
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)
            text = recognizer.recognize_google(audio, language="en-IN").lower()
            
            if wake_word in text:
                print(f"✅ Wake word detected!")
                print("🎤 Listening for command...")
                
               
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                command = recognizer.recognize_google(audio, language="en-IN")
                print(f"✅ Command: {command}")
                return command.lower()
            else:
                return "none"
        
        except:
            return "none"
