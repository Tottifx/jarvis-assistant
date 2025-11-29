import speech_recognition as sr
import pyttsx3
import threading
import time
from utils.logger import setup_logger

logger = setup_logger('speech_engine')

class SpeechEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.is_speaking = False
        self.setup_audio()
        logger.info("Speech engine initialized")
    
    def setup_audio(self):
        """Setup audio systems"""
        try:
            # Configure text-to-speech
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            
            # Setup microphone for ambient noise
            logger.info("Adjusting microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone setup complete")
            
        except Exception as e:
            logger.error(f"Audio setup error: {e}")
    
    def speak(self, text, wait=True):
        """Convert text to speech"""
        def _speak():
            self.is_speaking = True
            try:
                logger.info(f"JARVIS: {text}")
                self.tts_engine.say(text)
                if wait:
                    self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"Speech error: {e}")
            finally:
                self.is_speaking = False
        
        print(f"🤖 JARVIS: {text}")
        
        if wait:
            _speak()
        else:
            # Non-blocking speech
            thread = threading.Thread(target=_speak)
            thread.daemon = True
            thread.start()
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """Listen for voice command with timeout"""
        try:
            with self.microphone as source:
                logger.info("Listening...")
                print("🎤 Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            command = self.recognizer.recognize_google(audio).lower()
            logger.info(f"User said: {command}")
            print(f"👤 You: {command}")
            return command
            
        except sr.WaitTimeoutError:
            logger.info("Listening timeout")
            return ""
        except sr.UnknownValueError:
            logger.warning("Speech recognition could not understand audio")
            self.speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            self.speak("There seems to be a problem with speech recognition.")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error in listen: {e}")
            return ""
    
    def listen_continuous(self, stop_phrases=['stop listening', 'that\'s all']):
        """Listen continuously for longer commands"""
        self.speak("I'm listening continuously. Say 'stop listening' when you're done.")
        
        full_command = []
        while True:
            command = self.listen(timeout=10, phrase_time_limit=20)
            if not command:
                continue
            
            if any(phrase in command for phrase in stop_phrases):
                break
            
            full_command.append(command)
            self.speak("Got it. Continue or say 'stop listening' when done.")
        
        return " ".join(full_command)