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
        self.setup_english_audio()
        logger.info("Speech engine initialized")
    
    def setup_english_audio(self):
        """Setup audio systems with English voice"""
        try:
            # Get all available voices
            voices = self.tts_engine.getProperty('voices')
            logger.info(f"Found {len(voices)} available voices")
            
            # Find and set an English voice
            english_voice = None
            for voice in voices:
                logger.info(f"Voice: {voice.id} - {voice.name} - {voice.languages}")
                # Look for English voices (common patterns)
                if any(lang in str(voice.languages).lower() for lang in ['en', 'eng', 'english', 'en_us', 'en_gb']):
                    english_voice = voice
                    logger.info(f"Selected English voice: {voice.name}")
                    break
                # Also check voice name for English indicators
                elif any(indicator in voice.name.lower() for indicator in ['english', 'en_', 'us', 'gb', 'uk']):
                    english_voice = voice
                    logger.info(f"Selected English voice by name: {voice.name}")
                    break
            
            if english_voice:
                self.tts_engine.setProperty('voice', english_voice.id)
                logger.info(f"Set voice to: {english_voice.name}")
            else:
                # If no English voice found, use first available voice
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
                    logger.warning(f"No English voice found. Using default: {voices[0].name}")
                else:
                    logger.error("No voices available!")
            
            # Configure speech properties
            self.tts_engine.setProperty('rate', 170)  # Slightly faster for natural English
            self.tts_engine.setProperty('volume', 0.9)
            
            # Test the voice
            logger.info("Testing English voice...")
            
            # Setup microphone for ambient noise
            logger.info("Adjusting microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Microphone setup complete")
            
        except Exception as e:
            logger.error(f"Audio setup error: {e}")
            # Fallback: try basic initialization
            try:
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
            except:
                pass
    
    def speak(self, text, wait=True):
        """Convert text to speech with English pronunciation"""
        def _speak():
            self.is_speaking = True
            try:
                logger.info(f"JARVIS: {text}")
                
                # Pre-process text for better English pronunciation
                processed_text = self.preprocess_text(text)
                
                self.tts_engine.say(processed_text)
                if wait:
                    self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"Speech error: {e}")
                # Fallback: print to console
                print(f"JARVIS (Text): {text}")
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
    
    def preprocess_text(self, text):
        """Preprocess text for better English pronunciation"""
        # Replace common AI response artifacts
        replacements = {
            '```': '',  # Remove code blocks
            '**': '',   # Remove markdown bold
            '*': '',    # Remove markdown italics
            '#': '',    # Remove markdown headers
        }
        
        processed = text
        for old, new in replacements.items():
            processed = processed.replace(old, new)
        
        # Ensure proper spacing
        processed = ' '.join(processed.split())
        
        return processed
    
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
            
            # Use English language for recognition
            command = self.recognizer.recognize_google(audio, language='en-US').lower()
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
    
    def test_voice(self):
        """Test the current voice configuration"""
        test_phrases = [
            "Hello! I am JARVIS, your AI assistant.",
            "I am now speaking in English.",
            "How can I help you today?",
            "This is a test of the text to speech system."
        ]
        
        for phrase in test_phrases:
            print(f"Testing: {phrase}")
            self.speak(phrase)
            time.sleep(1)
    
    def get_voice_info(self):
        """Get information about current voice"""
        voice = self.tts_engine.getProperty('voice')
        rate = self.tts_engine.getProperty('rate')
        volume = self.tts_engine.getProperty('volume')
        
        return {
            'voice': voice,
            'rate': rate,
            'volume': volume
        }