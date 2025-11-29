#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.english_speech_engine import EnglishSpeechEngine as SpeechEngine
    print("Using English Speech Engine")
except ImportError:
    from core.speech_engine import SpeechEngine
    print("Using Standard Speech Engine")

def main():
    speech = SpeechEngine()
    
    print("🔊 Testing English Text-to-Speech")
    print("=" * 40)
    
    test_phrases = [
        "Hello! I am JARVIS, your AI assistant.",
        "I am speaking in clear English.",
        "How can I help you today?",
        "This is a test of the text to speech system.",
        "I can assist with programming, web searches, and more!"
    ]
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"{i}. {phrase}")
        speech.speak(phrase)
    
    print("\n✅ Voice test completed!")
    print("If you heard clear English speech, the setup is successful!")
    print("If not, we may need to install additional voice packages.")

if __name__ == "__main__":
    main()
