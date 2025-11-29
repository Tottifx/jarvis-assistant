import requests
import json
from config.api_keys import Config

class DeepSeekClient:
    def __init__(self):
        self.api_key = Config.DEEPSEEK_API_KEY
        self.api_url = Config.DEEPSEEK_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat(self, message, context="", personality="helpful assistant", temperature=0.7):
        """Main chat method with context and personality"""
        if not self.api_key:
            return "⚠️ Please set your DeepSeek API key in the .env file"
        
        system_message = f"""You are JARVIS, a friendly AI assistant. {personality}
        
        Context from previous conversation:
        {context}
        
        Be conversational, helpful, and concise in your responses."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ]
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2000,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ API Error {response.status_code}: {response.text}"
                
        except requests.exceptions.Timeout:
            return "❌ Request timeout. Please try again."
        except requests.exceptions.ConnectionError:
            return "❌ Connection error. Please check your internet connection."
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def programming_help(self, problem, language="python", context=""):
        """Specialized programming help"""
        personality = "expert programming tutor who explains concepts clearly with practical examples and code snippets"
        
        prompt = f"""
        Programming Help Request:
        Language: {language}
        Problem: {problem}
        
        Please provide:
        1. Clear solution with code example
        2. Step-by-step explanation
        3. Best practices
        4. Common pitfalls to avoid
        5. Alternative approaches if applicable
        
        Keep it practical and actionable. Format code properly.
        """
        
        return self.chat(prompt, context, personality, temperature=0.3)
    
    def debug_code(self, code, error_message, language="python"):
        """Debug specific code with error message"""
        prompt = f"""
        Debug this {language} code:
        
        Code:
        {code}
        
        Error:
        {error_message}
        
        Please:
        1. Identify the exact problem
        2. Explain why the error occurs
        3. Provide the corrected code
        4. Explain the fix
        """
        
        return self.chat(prompt, personality="expert debugger and programming mentor")
    
    def friend_chat(self, message, context=""):
        """Friendly conversation mode"""
        personality = "caring friend who listens well, shows empathy, remembers details, and engages in meaningful conversation. Be warm and supportive."
        return self.chat(message, context, personality, temperature=0.8)