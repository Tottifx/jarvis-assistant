#!/usr/bin/env python3
import os
import sys
import signal

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try importing English speech engine first, fallback to standard
try:
    from core.english_speech_engine import EnglishSpeechEngine as SpeechEngine
    print("✅ Using English Speech Engine")
except ImportError:
    try:
        from core.speech_engine import SpeechEngine
        print("✅ Using Standard Speech Engine")
    except ImportError:
        print("❌ No speech engine found. Creating basic fallback...")
        # Create a basic fallback speech engine
        class BasicSpeechEngine:
            def speak(self, text, wait=True):
                print(f"🤖 JARVIS: {text}")
            def listen(self, timeout=5):
                return input("👤 You (type your command): ").lower()
        SpeechEngine = BasicSpeechEngine

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
        
        # Test English voice on startup
        self.test_english_voice()
        
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
        
        # User info
        self.user_name = self.memory.memory["user_info"]["name"]
        
        print("✅ JARVIS initialized successfully!")
        print(f"🌐 Online mode: {self.online_mode}")
        print(f"👤 User: {self.user_name if self.user_name else 'Not set'}")
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def test_english_voice(self):
        """Test that the voice is working in English"""
        print("🔊 Testing English voice...")
        test_phrases = [
            "Hello! I am JARVIS, your AI assistant.",
            "I am now speaking in clear English.",
            "Ready to help with programming and more!"
        ]
        
        for phrase in test_phrases:
            print(f"Testing: {phrase}")
            self.speech.speak(phrase)
    
    def setup_command_keywords(self):
        """Setup command keywords for intent classification"""
        self.programming_keywords = [
            'code', 'program', 'programming', 'python', 'javascript', 'java', 'c++', 'cpp', 'c#',
            'error', 'bug', 'debug', 'fix', 'function', 'class', 'variable', 'loop', 'array',
            'syntax', 'compile', 'run', 'execute', 'algorithm', 'data structure', 'import',
            'def ', 'print', 'return', 'if ', 'for ', 'while ', 'try ', 'except'
        ]
        
        self.web_keywords = [
            'search', 'browse', 'open', 'website', 'internet', 'google', 'youtube',
            'github', 'stack overflow', 'wikipedia', 'look up', 'find', 'browser'
        ]
        
        self.friend_keywords = [
            'hello', 'hi', 'hey', 'how are you', 'your name', 'friend', 'chat',
            'talk', 'feeling', 'mood', 'happy', 'sad', 'angry', 'tired', 'bored',
            'excited', 'nice to meet you', 'good morning', 'good afternoon', 'good evening'
        ]
        
        self.system_keywords = [
            'offline', 'online', 'mode', 'switch', 'language', 'help', 'what can you do',
            'status', 'reset', 'clear', 'memory', 'settings'
        ]
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.speech.speak("Goodbye! Shutting down now.")
        # Save memory before exiting
        self.memory.save_memory()
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
        
        # Extract language if specified
        language = self.current_language
        for lang in ['python', 'javascript', 'java', 'c++', 'cpp', 'c#']:
            if lang in command.lower():
                language = lang
                break
        
        if self.online_mode:
            # Use AI for detailed programming help
            context = self.memory.get_recent_context()
            programming_context = self.memory.get_programming_context(language)
            full_context = f"{context}\nProgramming knowledge: {programming_context}"
            
            response = self.ai.programming_help(command, language, full_context)
            
            # Store the solution in memory for future reference
            if "error" in command.lower() or "fix" in command.lower():
                self.memory.add_programming_knowledge(language, command, response)
        else:
            # Use offline programming helper
            response = self.programming.handle_programming_request(command, language)
        
        return response
    
    def handle_web_request(self, command):
        """Handle web-related requests"""
        if not self.online_mode:
            return "Web features require online mode. Please enable online mode to search the web."
        
        command_lower = command.lower()
        
        if 'open' in command_lower:
            site = command_lower.replace('open', '').strip()
            response = self.web_surf.open_website(site)
        elif 'search' in command_lower:
            query = command_lower.replace('search', '').replace('for', '').strip()
            response = self.web_surf.search_web(query)
        elif 'browse' in command_lower:
            topic = command_lower.replace('browse', '').replace('for', '').strip()
            response = self.web_surf.get_quick_info(topic)
        else:
            # Assume it's a search query
            response = self.web_surf.search_web(command)
        
        return response
    
    def handle_friend_mode(self, command):
        """Handle friendly conversation"""
        # First check for personal responses
        personal_response = self.friend.get_personal_response(command)
        if personal_response:
            return personal_response
        
        # Update user info if name is mentioned
        if 'my name is' in command.lower():
            name = command.lower().split('my name is')[-1].strip().title()
            self.user_name = name
            self.memory.set_user_info(name)
            return f"Nice to meet you, {name}! I'll remember that. What would you like to talk about?"
        
        if self.online_mode:
            # Use AI for deeper conversation with memory context
            context = self.memory.get_recent_context()
            user_info = f"User name: {self.user_name}" if self.user_name else ""
            full_context = f"{context}\n{user_info}"
            
            return self.ai.friend_chat(command, full_context)
        else:
            return self.friend.offline_chat(command)
    
    def handle_system_commands(self, command):
        """Handle system-level commands"""
        command_lower = command.lower()
        
        if 'online mode' in command_lower or 'switch to online' in command_lower:
            self.online_mode = True
            return "Switched to online mode. AI features are now available."
        
        elif 'offline mode' in command_lower or 'switch to offline' in command_lower:
            self.online_mode = False
            return "Switched to offline mode. Using local programming knowledge."
        
        elif 'language' in command_lower:
            if 'python' in command_lower:
                self.current_language = 'python'
            elif 'javascript' in command_lower or 'js' in command_lower:
                self.current_language = 'javascript'
            elif 'java' in command_lower:
                self.current_language = 'java'
            elif 'c++' in command_lower or 'cpp' in command_lower:
                self.current_language = 'cpp'
            elif 'c#' in command_lower or 'c sharp' in command_lower:
                self.current_language = 'c#'
            else:
                return f"Current language is {self.current_language}. Available languages: Python, JavaScript, Java, C++, C#"
            
            return f"Programming language set to {self.current_language}"
        
        elif 'status' in command_lower or 'info' in command_lower:
            status_info = f"""
Current Status:
- Online Mode: {'Enabled 🌐' if self.online_mode else 'Disabled 🔌'}
- Programming Language: {self.current_language}
- User: {self.user_name if self.user_name else 'Not set'}
- Total Interactions: {self.memory.memory['system_data']['total_interactions']}
"""
            return status_info
        
        elif 'help' in command_lower or 'what can you do' in command_lower:
            return self.get_help_message()
        
        elif 'clear memory' in command_lower or 'reset' in command_lower:
            # Reset conversation history but keep user info
            self.memory.memory["conversation_history"] = []
            self.memory.save_memory()
            return "Conversation history cleared. Your user information is still saved."
        
        else:
            return "I didn't understand that system command. Try 'online mode', 'offline mode', 'status', or 'help'."
    
    def get_help_message(self):
        """Get help information"""
        help_text = """
JARVIS AI Assistant - Help Guide

I can help you with:

PROGRAMMING HELP:
- "Fix this Python error: [error description]"
- "Explain functions in JavaScript"
- "How to create a class in Python"
- "Debug my code: [code snippet]"
- "What is a list comprehension?"

WEB SURFING (Online only):
- "Search for artificial intelligence"
- "Open GitHub"
- "Browse Python tutorials"
- "Search Wikipedia for machine learning"

FRIEND MODE:
- "Hello, my name is [Your Name]"
- "How are you today?"
- "Tell me a fun fact"
- "I need motivation"
- "What's your name?"

SYSTEM COMMANDS:
- "Switch to online mode" - Enable AI features
- "Switch to offline mode" - Use local knowledge only
- "Set language to Python/JavaScript/Java/C++"
- "Status" - Show current settings
- "Help" - Show this message
- "Clear memory" - Reset conversation history

MEMORY: I remember our conversations and your preferences!

Say 'exit', 'quit', or 'goodbye' to stop.
"""
        return help_text
    
    def handle_general(self, command):
        """Handle general questions"""
        if self.online_mode:
            context = self.memory.get_recent_context()
            return self.ai.chat(command, context)
        else:
            # Provide more helpful offline responses
            if 'what' in command.lower() and 'you' in command.lower():
                return "I'm JARVIS, your AI assistant! I can help with programming, answer questions when online, or just chat with you."
            elif 'who are you' in command.lower():
                return "I'm JARVIS, your personal AI assistant. I can help with programming, web searches, and general conversation when in online mode."
            else:
                return "That's an interesting question! For detailed answers, please enable online mode. I can still help with programming questions in offline mode."
    
    def process_command(self, command):
        """Process and route commands"""
        if not command:
            return None
        
        # Clean the command
        command = command.strip()
        
        # Check for exit commands
        if any(word in command.lower() for word in ['exit', 'quit', 'goodbye', 'bye', 'stop', 'shutdown']):
            self.speech.speak("Goodbye! It was great talking with you!")
            # Save memory before exiting
            self.memory.save_memory()
            return 'exit'
        
        # Check for special commands
        if 'fun fact' in command.lower():
            response = self.friend.share_fun_fact()
            self.speech.speak(response)
            self.memory.add_conversation(command, response)
            return None
        
        if 'motivation' in command.lower() or 'quote' in command.lower() or 'inspire' in command.lower():
            response = self.friend.get_motivational_quote()
            self.speech.speak(response)
            self.memory.add_conversation(command, response)
            return None
        
        if 'thank' in command.lower():
            responses = [
                "You're welcome!",
                "Happy to help!",
                "Anytime!",
                "Glad I could assist!"
            ]
            import random
            response = random.choice(responses)
            self.speech.speak(response)
            self.memory.add_conversation(command, response)
            return None
        
        # Classify and handle intent
        intent = self.classify_intent(command)
        
        try:
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
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error processing your request: {str(e)}"
            print(f"Error: {e}")
            self.speech.speak("Sorry, I encountered an error. Please try again.")
            self.memory.add_conversation(command, "Error occurred")
        
        return None
    
    def run(self):
        """Main application loop"""
        welcome_message = """
🤖 JARVIS AI Assistant Started!
💻 Programming Help | 🌐 Web Surfing | 👥 Friend Mode
💾 Memory: I remember our conversations!
🔌 Current Mode: {}        
👤 User: {}
        """.format(
            "ONLINE 🌐" if self.online_mode else "OFFLINE 🔌",
            self.user_name if self.user_name else "Not set (say 'my name is [name]')"
        )
        
        print(welcome_message)
        
        # Personalized greeting
        if self.user_name:
            greeting = f"Hello {self.user_name}! I'm JARVIS, ready to help you with programming, web searches, or just chat!"
        else:
            greeting = "Hello! I'm JARVIS, your AI assistant. You can tell me your name by saying 'my name is [your name]'. I can help with programming, web searches, or just be a friend to chat with!"
        
        self.speech.speak(greeting)
        
        # Main interaction loop
        interaction_count = 0
        while True:
            try:
                # Listen for command with increasing timeout for first few interactions
                timeout = 8 if interaction_count < 3 else 5
                command = self.speech.listen(timeout=timeout)
                interaction_count += 1
                
                if command:
                    result = self.process_command(command)
                    if result == 'exit':
                        break
                else:
                    # No command heard for a while
                    if interaction_count > 2:  # After initial setup
                        print("💤 I'm listening... Say 'help' for options or 'exit' to quit.")
                
            except KeyboardInterrupt:
                print("\n🛑 Keyboard interrupt received.")
                self.speech.speak("Shutting down. Goodbye!")
                break
            except Exception as e:
                error_msg = f"Unexpected error in main loop: {e}"
                print(error_msg)
                # Don't speak the error to avoid TTS issues, just continue
                continue
        
        # Final cleanup
        print("\n👋 JARVIS session ended.")
        print(f"📊 Total interactions this session: {interaction_count}")

if __name__ == "__main__":
    # Check for basic dependencies
    try:
        import speech_recognition
        print("✅ speech_recognition available")
    except ImportError as e:
        print(f"❌ Missing speech_recognition: {e}")
    
    try:
        import pyttsx3
        print("✅ pyttsx3 available")
    except ImportError as e:
        print(f"⚠️  pyttsx3 not available: {e}")
    
    try:
        import requests
        print("✅ requests available")
    except ImportError as e:
        print(f"⚠️  requests not available: {e}")
    
    # Create data directories
    os.makedirs('data/logs', exist_ok=True)
    os.makedirs('data/temp', exist_ok=True)
    
    # Check if .env exists, if not create from example
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("📝 Creating .env file from template...")
            with open('.env.example', 'r') as example:
                with open('.env', 'w') as env_file:
                    env_file.write(example.read())
            print("✅ Please edit .env file with your DeepSeek API key")
        else:
            print("📝 Creating basic .env file...")
            with open('.env', 'w') as env_file:
                env_file.write("""# DeepSeek API Configuration
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Application Mode
OFFLINE_MODE=false

# Speech Settings
SPEECH_RATE=170
SPEECH_VOLUME=0.9

# Memory Settings
MAX_CONVERSATION_HISTORY=20
""")
            print("✅ Created .env file. Please edit it with your DeepSeek API key")
    
    # Check for API key if online mode is enabled
    from config.api_keys import Config
    if not Config.OFFLINE_MODE and not Config.DEEPSEEK_API_KEY:
        print("⚠️  Warning: Online mode enabled but no DeepSeek API key found.")
        print("💡 You can:")
        print("   1. Add your API key to the .env file")
        print("   2. Set OFFLINE_MODE=true in .env file")
        print("   3. Continue with limited offline functionality")
        input("Press Enter to continue...")
    
    try:
        jarvis = JARVIS()
        jarvis.run()
    except Exception as e:
        print(f"❌ Failed to start JARVIS: {e}")
        print("💡 Troubleshooting tips:")
        print("   - Check if all dependencies are installed: pip install -r requirements.txt")
        print("   - Verify microphone is working")
        print("   - Check .env file configuration")
        print("   - Try running: python test_voice.py")