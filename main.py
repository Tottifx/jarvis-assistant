#!/usr/bin/env python3
import os
import sys
import signal

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.speech_engine import SpeechEngine
from core.memory import MemorySystem
from ai.deepseek_client import DeepSeekClient
from modules.programming_helper import ProgrammingHelper
from modules.web_surf import WebSurfer
from modules.friend_mode import FriendMode
from modules.offline_coder import OfflineCoder
from config.api_keys import Config

class JARVIS:
    def __init__(self):
        print("🚀 Initializing JARVIS AI Assistant...")
        
        # Initialize core systems
        self.speech = SpeechEngine()
        self.memory = MemorySystem()
        
        # Initialize AI clients
        self.ai = DeepSeekClient()
        self.offline_coder = OfflineCoder(self.memory)
        
        # Initialize modules
        self.programming = ProgrammingHelper(self.memory, self.offline_coder)
        self.web_surf = WebSurfer(self.memory)
        self.friend = FriendMode(self.memory)
        
        # Mode settings
        self.online_mode = not Config.OFFLINE_MODE
        self.current_language = 'python'
        
        # Command keywords for intent classification
        self.setup_command_keywords()
        
        print("✅ JARVIS initialized successfully!")
        print(f"🌐 Online mode: {self.online_mode}")
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def setup_command_keywords(self):
        """Setup command keywords for intent classification"""
        self.programming_keywords = [
            'code', 'program', 'programming', 'python', 'javascript', 'java', 'c++', 'cpp',
            'error', 'bug', 'debug', 'fix', 'function', 'class', 'variable', 'loop',
            'syntax', 'compile', 'run', 'execute', 'algorithm', 'data structure'
        ]
        
        self.web_keywords = [
            'search', 'browse', 'open', 'website', 'internet', 'google', 'youtube',
            'github', 'stack overflow', 'wikipedia', 'look up', 'find'
        ]
        
        self.friend_keywords = [
            'hello', 'hi', 'hey', 'how are you', 'your name', 'friend', 'chat',
            'talk', 'feeling', 'mood', 'happy', 'sad', 'angry', 'tired'
        ]
        
        self.system_keywords = [
            'offline', 'online', 'mode', 'switch', 'language', 'help', 'what can you do'
        ]
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.speech.speak("Goodbye! Shutting down now.")
        sys.exit(0)
    
    def classify_intent(self, command):
        """Classify user intent from command"""
        command_lower = command.lower()
        
        if any(keyword in command_lower for keyword in self.programming_keywords):
            return 'programming'
        elif any(keyword in command_lower for keyword in self.web_keywords):
            return 'web'
        elif any(keyword in command_lower for keyword in self.friend_keywords):
            return 'friend'
        elif any(keyword in command_lower for keyword in self.system_keywords):
            return 'system'
        else:
            return 'general'
    
    def handle_programming(self, command):
        """Handle programming-related requests"""
        self.speech.speak("I'll help with your programming question!")
        
        if self.online_mode:
            # Use AI for detailed programming help
            context = self.memory.get_recent_context()
            response = self.ai.programming_help(command, self.current_language, context)
        else:
            # Use offline programming helper
            response = self.programming.handle_programming_request(command, self.current_language)
        
        return response
    
    def handle_web_request(self, command):
        """Handle web-related requests"""
        if not self.online_mode:
            return "🌐 Web features require online mode. Please enable online mode to search the web."
        
        if 'open' in command.lower():
            site = command.lower().replace('open', '').strip()
            response = self.web_surf.open_website(site)
        elif 'search' in command.lower():
            query = command.lower().replace('search', '').replace('for', '').strip()
            response = self.web_surf.search_web(query)
        else:
            response = self.web_surf.get_quick_info(command)
        
        return response
    
    def handle_friend_mode(self, command):
        """Handle friendly conversation"""
        # First check for personal responses
        personal_response = self.friend.get_personal_response(command)
        if personal_response:
            return personal_response
        
        if self.online_mode:
            # Use AI for deeper conversation
            context = self.memory.get_recent_context()
            return self.ai.friend_chat(command, context)
        else:
            return self.friend.offline_chat(command)
    
    def handle_system_commands(self, command):
        """Handle system-level commands"""
        command_lower = command.lower()
        
        if 'online mode' in command_lower:
            self.online_mode = True
            return "✅ Switched to online mode. AI features are now available."
        
        elif 'offline mode' in command_lower:
            self.online_mode = False
            return "🔌 Switched to offline mode. Using local programming knowledge."
        
        elif 'language' in command_lower:
            if 'python' in command_lower:
                self.current_language = 'python'
            elif 'javascript' in command_lower:
                self.current_language = 'javascript'
            elif 'java' in command_lower:
                self.current_language = 'java'
            elif 'c++' in command_lower or 'cpp' in command_lower:
                self.current_language = 'cpp'
            return f"🗣️ Programming language set to {self.current_language}"
        
        elif 'help' in command_lower or 'what can you do' in command_lower:
            return self.get_help_message()
        
        else:
            return "🤔 I didn't understand that system command. Try 'online mode', 'offline mode', or 'help'."
    
    def get_help_message(self):
        """Get help information"""
        help_text = """
🤖 JARVIS AI Assistant - Help Guide

I can help you with:

💻 PROGRAMMING HELP:
  - "Fix this Python error"
  - "Explain functions in JavaScript"
  - "How to create a class in Python"
  - "Debug my code"

🌐 WEB SURFING (Online only):
  - "Search for artificial intelligence"
  - "Open GitHub"
  - "Browse Python tutorials"

👥 FRIEND MODE:
  - "Hello, my name is [Your Name]"
  - "How are you today?"
  - "Tell me a fun fact"
  - "I need motivation"

⚙️ SYSTEM COMMANDS:
  - "Switch to online mode"
  - "Switch to offline mode"
  - "Set language to Python/JavaScript"
  - "Help" - Show this message

💾 MEMORY: I remember our conversations and your preferences!

Say 'exit' or 'quit' to stop.
"""
        return help_text
    
    def handle_general(self, command):
        """Handle general questions"""
        if self.online_mode:
            context = self.memory.get_recent_context()
            return self.ai.chat(command, context)
        else:
            return "💬 I'd love to chat! For general conversations, please enable online mode for AI-powered responses."
    
    def process_command(self, command):
        """Process and route commands"""
        if not command:
            return
        
        # Check for exit commands
        if any(word in command for word in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
            self.speech.speak("Goodbye! It was great talking with you!")
            return 'exit'
        
        # Check for special commands
        if 'fun fact' in command.lower():
            response = self.friend.share_fun_fact()
            self.speech.speak(response)
            self.memory.add_conversation(command, response)
            return
        
        if 'motivation' in command.lower() or 'quote' in command.lower():
            response = self.friend.get_motivational_quote()
            self.speech.speak(response)
            self.memory.add_conversation(command, response)
            return
        
        # Classify and handle intent
        intent = self.classify_intent(command)
        
        if intent == 'programming':
            response = self.handle_programming(command)
        elif intent == 'web':
            response = self.handle_web_request(command)
        elif intent == 'friend':
            response = self.handle_friend_mode(command)
        elif intent == 'system':
            response = self.handle_system_commands(command)
        else:
            response = self.handle_general(command)
        
        # Speak response and store in memory
        self.speech.speak(response)
        self.memory.add_conversation(command, response)
    
    def run(self):
        """Main application loop"""
        welcome_message = """
🤖 JARVIS AI Assistant Started!
💻 Programming Help | 🌐 Web Surfing | 👥 Friend Mode
💾 Memory: I remember our conversations!
🔌 Current Mode: {}        
        """.format("ONLINE 🌐" if self.online_mode else "OFFLINE 🔌")
        
        print(welcome_message)
        self.speech.speak("Hello! I'm JARVIS, your AI assistant. I can help with programming, web searches, or just be a friend to chat with!")
        
        while True:
            try:
                command = self.speech.listen()
                
                if command:
                    result = self.process_command(command)
                    if result == 'exit':
                        break
                else:
                    # No command heard, you can add a timeout message here
                    pass
                
            except KeyboardInterrupt:
                print("\n🛑 Keyboard interrupt received.")
                self.speech.speak("Shutting down. Goodbye!")
                break
            except Exception as e:
                error_msg = f"Unexpected error: {e}"
                print(error_msg)
                self.speech.speak("Sorry, I encountered an error. Let's continue.")

if __name__ == "__main__":
    # Check for basic dependencies
    try:
        import speech_recognition
        import pyttsx3
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please run: pip install -r requirements.txt")
        exit(1)
    
    # Create data directories
    os.makedirs('data/logs', exist_ok=True)
    os.makedirs('data/temp', exist_ok=True)
    
    # Check if .env exists, if not create from example
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        print("📝 Creating .env file from template...")
        with open('.env.example', 'r') as example:
            with open('.env', 'w') as env_file:
                env_file.write(example.read())
        print("✅ Please edit .env file with your DeepSeek API key")
    
    jarvis = JARVIS()
    jarvis.run()