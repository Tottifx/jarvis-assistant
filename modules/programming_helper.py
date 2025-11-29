import subprocess
import os
import tempfile
from utils.logger import setup_logger

logger = setup_logger('programming_helper')

class ProgrammingHelper:
    def __init__(self, memory_system, offline_coder):
        self.memory = memory_system
        self.offline_coder = offline_coder
    
    def handle_programming_request(self, request, language='python'):
        """Handle programming requests with offline first approach"""
        logger.info(f"Programming request: {request} for {language}")
        
        # Store programming interest in memory
        self.memory.add_programming_knowledge(language, request)
        
        # Analyze request type
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['error', 'bug', 'fix', 'debug']):
            return self.handle_debug_request(request, language)
        elif any(word in request_lower for word in ['how to', 'create', 'make', 'build']):
            return self.handle_howto_request(request, language)
        elif any(word in request_lower for word in ['explain', 'what is', 'concept']):
            return self.handle_explanation_request(request, language)
        elif any(word in request_lower for word in ['example', 'code sample']):
            return self.handle_example_request(request, language)
        else:
            return self.handle_general_request(request, language)
    
    def handle_debug_request(self, request, language):
        """Handle debugging requests"""
        # Extract code and error from request (basic pattern matching)
        code_match = re.search(r'code[:\s]*(.*?)(?=error|$)', request, re.IGNORECASE | re.DOTALL)
        error_match = re.search(r'error[:\s]*(.*?)(?=code|$)', request, re.IGNORECASE | re.DOTALL)
        
        if code_match and error_match:
            code = code_match.group(1).strip()
            error = error_match.group(1).strip()
            
            # First try offline analysis
            analysis = self.offline_coder.analyze_code(code, language)
            if analysis['status'] == 'invalid':
                offline_fix = self.offline_coder.suggest_python_fix(analysis['message'])
                response = f"🔧 Offline Analysis:\n{analysis['message']}\n💡 Suggestion: {offline_fix}"
            else:
                response = "🔍 I analyzed your code offline. For detailed debugging with AI, please enable online mode."
            
            return response
        else:
            return "🤔 I can help debug your code. Please share both the code and the error message for better assistance."
    
    def handle_howto_request(self, request, language):
        """Handle how-to programming questions"""
        # Try offline templates first
        if 'function' in request.lower():
            template = self.offline_coder.generate_code_template('function', language)
            return f"📝 Here's a basic function template in {language}:\n\n```{language}\n{template}\n```"
        elif 'class' in request.lower():
            template = self.offline_coder.generate_code_template('class', language)
            return f"📝 Here's a basic class template in {language}:\n\n```{language}\n{template}\n```"
        elif 'loop' in request.lower():
            template = self.offline_coder.generate_code_template('loop', language)
            return f"📝 Here's a basic loop template in {language}:\n\n```{language}\n{template}\n```"
        else:
            return f"💡 I can help with {language} programming. For specific how-to guidance, please enable online mode for AI assistance."
    
    def handle_explanation_request(self, request, language):
        """Handle concept explanation requests"""
        # Extract concept from request
        concepts = ['list comprehension', 'dictionary', 'function', 'class', 'inheritance', 'decorator']
        found_concept = None
        for concept in concepts:
            if concept in request.lower():
                found_concept = concept
                break
        
        if found_concept:
            return self.offline_coder.explain_concept(found_concept, language)
        else:
            return "📚 I can explain programming concepts offline. Try asking about: functions, classes, loops, or specific language features."
    
    def handle_example_request(self, request, language):
        """Handle code example requests"""
        return "💻 I can provide code examples. Please enable online mode for comprehensive code samples with explanations."
    
    def handle_general_request(self, request, language):
        """Handle general programming requests"""
        return f"💬 I can help with {language} programming including debugging, explanations, and code examples. For detailed AI assistance, enable online mode."
    
    def run_code_safely(self, code, language='python'):
        """Safely run code in isolated environment"""
        if language != 'python':
            return "❌ Only Python code can be executed safely in this version."
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Execute with timeout
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=10  # 10 second timeout
            )
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return f"✅ Code executed successfully!\nOutput:\n{result.stdout}"
            else:
                return f"❌ Error executing code:\n{result.stderr}"
                
        except subprocess.TimeoutExpired:
            os.unlink(temp_file)
            return "❌ Code execution timed out (possibly infinite loop)"
        except Exception as e:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            return f"❌ Execution error: {str(e)}"