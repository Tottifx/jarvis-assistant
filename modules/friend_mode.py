import random
from datetime import datetime

class FriendMode:
    def __init__(self, memory_system):
        self.memory = memory_system
    
    def get_personal_response(self, message):
        """Generate personal, friendly responses"""
        message_lower = message.lower()
        
        # Greetings
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            name = self.memory.memory["user_info"]["name"]
            if name:
                return random.choice([
                    f"Hey {name}! Great to hear from you!",
                    f"Hello {name}! How's your day going?",
                    f"Hi {name}! What's on your mind today?"
                ])
            else:
                return random.choice([
                    "Hello there! I'm JARVIS, your AI friend!",
                    "Hey! Nice to meet you! I'm here to help and chat.",
                    "Hi! I'm JARVIS. What should I call you?"
                ])
        
        elif 'your name' in message_lower:
            return "I'm JARVIS! Your AI assistant and friend. What's your name?"
        
        elif 'my name is' in message_lower:
            name = message_lower.split('my name is')[-1].strip()
            self.memory.set_user_info(name)
            return f"Nice to meet you, {name}! I'll remember that. What would you like to talk about?"
        
        elif 'how are you' in message_lower:
            return random.choice([
                "I'm doing great! Thanks for asking. How about you?",
                "I'm wonderful! Always happy to chat with you.",
                "Doing well! Ready to help with anything you need."
            ])
        
        return None
    
    def share_fun_fact(self):
        """Share a random fun fact"""
        facts = [
            "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!",
            "Fun fact: Octopuses have three hearts! Two pump blood through the gills, while the third pumps it through the body.",
            "Interesting: The shortest war in history was between Britain and Zanzibar in 1896. It lasted only 38 minutes!",
            "Cool fact: Bananas are berries, but strawberries aren't!",
            "Did you know? A day on Venus is longer than a year on Venus."
        ]
        return random.choice(facts)
    
    def get_motivational_quote(self):
        """Share a motivational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "It's not whether you get knocked down, it's whether you get up. - Vince Lombardi",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
            "Believe you can and you're halfway there. - Theodore Roosevelt"
        ]
        return random.choice(quotes)
    
    def offline_chat(self, message):
        """Basic offline chat responses"""
        responses = [
            "That's interesting! Tell me more.",
            "I'd love to hear more about that.",
            "How does that make you feel?",
            "That sounds important to you.",
            "I'm here to listen and help however I can."
        ]
        return random.choice(responses)