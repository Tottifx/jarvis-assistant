import json
import os
from datetime import datetime
from config.api_keys import Config

class MemorySystem:
    def __init__(self):
        self.memory_file = Config.MEMORY_FILE
        self.memory = self.load_memory()
    
    def load_memory(self):
        """Load conversation memory from file"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
        
        # Initialize empty memory structure
        return {
            "user_info": {
                "name": "",
                "preferences": {},
                "programming_languages": []
            },
            "conversation_history": [],
            "learned_facts": {},
            "programming_knowledge": {
                "python": {"errors_fixed": [], "concepts_learned": []},
                "javascript": {"errors_fixed": [], "concepts_learned": []},
                "java": {"errors_fixed": [], "concepts_learned": []},
                "cpp": {"errors_fixed": [], "concepts_learned": []}
            },
            "friendship_data": {
                "user_mood": "",
                "favorite_topics": [],
                "personal_details": {}
            },
            "system_data": {
                "last_session": "",
                "total_interactions": 0
            }
        }
    
    def save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving memory: {e}")
            return False
    
    def add_conversation(self, user_input, assistant_response):
        """Add conversation to history with timestamp"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": assistant_response,
            "type": "conversation"
        }
        
        self.memory["conversation_history"].append(conversation)
        self.memory["system_data"]["total_interactions"] += 1
        self.memory["system_data"]["last_session"] = datetime.now().isoformat()
        
        # Keep only recent conversations
        if len(self.memory["conversation_history"]) > Config.MAX_CONVERSATION_HISTORY:
            self.memory["conversation_history"] = self.memory["conversation_history"][-Config.MAX_CONVERSATION_HISTORY:]
        
        self.save_memory()
    
    def add_programming_knowledge(self, language, concept, solution=None):
        """Add programming knowledge"""
        if language not in self.memory["programming_knowledge"]:
            self.memory["programming_knowledge"][language] = {"errors_fixed": [], "concepts_learned": []}
        
        if solution:
            self.memory["programming_knowledge"][language]["errors_fixed"].append({
                "concept": concept,
                "solution": solution,
                "timestamp": datetime.now().isoformat()
            })
        else:
            self.memory["programming_knowledge"][language]["concepts_learned"].append({
                "concept": concept,
                "timestamp": datetime.now().isoformat()
            })
        
        self.save_memory()
    
    def get_recent_context(self, num_conversations=5):
        """Get recent conversation context"""
        recent = self.memory["conversation_history"][-num_conversations:]
        context = []
        for conv in recent:
            context.append(f"User: {conv['user']}")
            context.append(f"Assistant: {conv['assistant']}")
        return "\n".join(context)
    
    def get_programming_context(self, language):
        """Get programming knowledge for specific language"""
        if language in self.memory["programming_knowledge"]:
            return self.memory["programming_knowledge"][language]
        return {"errors_fixed": [], "concepts_learned": []}
    
    def set_user_info(self, name, preferences=None):
        """Set user information"""
        self.memory["user_info"]["name"] = name
        if preferences:
            self.memory["user_info"]["preferences"].update(preferences)
        self.save_memory()