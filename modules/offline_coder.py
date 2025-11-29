import ast
import re
import keyword
from utils.logger import setup_logger

logger = setup_logger('offline_coder')

class OfflineCoder:
    def __init__(self, memory_system):
        self.memory = memory_system
        self.setup_programming_knowledge()
    
    def setup_programming_knowledge(self):
        """Initialize offline programming knowledge base"""
        self.language_syntax = {
            'python': {
                'data_types': ['int', 'float', 'str', 'bool', 'list', 'tuple', 'dict', 'set'],
                'keywords': keyword.kwlist,
                'common_errors': {
                    'syntax_error': 'Check for missing colons, parentheses, or incorrect indentation',
                    'name_error': 'Variable might not be defined or has a typo',
                    'type_error': 'Check if you are using the right data types',
                    'index_error': 'You are accessing an element that does not exist in the list',
                    'key_error': 'The key does not exist in the dictionary',
                    'indentation_error': 'Check your code indentation (use 4 spaces per level)'
                }
            },
            'javascript': {
                'data_types': ['let', 'const', 'var', 'function', 'class'],
                'keywords': ['function', 'class', 'if', 'else', 'for', 'while', 'return'],
                'common_errors': {
                    'undefined': 'Variable used before declaration',
                    'type_error': 'Incompatible type operation',
                    'syntax_error': 'Check for missing brackets or semicolons'
                }
            }
        }
        
        self.code_templates = {
            'python': {
                'function': "def function_name(parameters):\n    # Your code here\n    return result",
                'class': "class ClassName:\n    def __init__(self, parameters):\n        self.attributes = parameters\n    \n    def method_name(self):\n        # Method code",
                'loop': "for item in collection:\n    # Process item\n\n# Or while loop:\nwhile condition:\n    # Loop code",
                'conditional': "if condition:\n    # Code if true\nelif other_condition:\n    # Code if other true\nelse:\n    # Code if all false"
            }
        }
    
    def analyze_code(self, code, language='python'):
        """Basic code analysis without executing"""
        try:
            if language == 'python':
                # Try to parse Python code
                ast.parse(code)
                return {"status": "valid", "message": "Code syntax appears valid"}
            else:
                return {"status": "unknown", "message": "Language analysis not available offline"}
                
        except SyntaxError as e:
            error_info = {
                "status": "invalid",
                "error_type": "SyntaxError",
                "message": str(e),
                "suggestion": self.suggest_python_fix(str(e))
            }
            return error_info
        except Exception as e:
            return {"status": "error", "message": f"Analysis error: {str(e)}"}
    
    def suggest_python_fix(self, error_message):
        """Suggest fixes for common Python errors"""
        error_lower = error_message.lower()
        
        if 'unexpected indent' in error_lower:
            return "Remove extra indentation or check consistent use of spaces/tabs"
        elif 'expected colon' in error_lower:
            return "Add colon (:) at the end of function/class/if/for/while statements"
        elif 'parenthesis' in error_lower:
            return "Check for matching parentheses, brackets, or braces"
        elif 'invalid syntax' in error_lower:
            return "Check for typos, missing operators, or incorrect keyword usage"
        elif 'name' in error_lower and 'is not defined' in error_lower:
            return "Variable might be misspelled or defined after use. Check variable names."
        elif 'indentation' in error_lower:
            return "Ensure consistent indentation (4 spaces recommended)"
        else:
            return "Review the code for syntax errors and check documentation"
    
    def generate_code_template(self, pattern, language='python'):
        """Generate code templates for common patterns"""
        if language in self.code_templates and pattern in self.code_templates[language]:
            return self.code_templates[language][pattern]
        return "Code template not available for this pattern/language"
    
    def explain_concept(self, concept, language='python'):
        """Explain programming concepts offline"""
        concepts = {
            'python': {
                'list comprehension': "A concise way to create lists: [expression for item in list if condition]",
                'dictionary': "Key-value pairs: {key1: value1, key2: value2}",
                'function': "Reusable code block: def name(params): return value",
                'class': "Blueprint for objects with attributes and methods",
                'inheritance': "One class inherits attributes/methods from another",
                'decorator': "Function that modifies another function"
            },
            'javascript': {
                'function': "function name(params) { return value; } or const name = (params) => value",
                'class': "class Name { constructor() {} method() {} }",
                'promise': "Object representing eventual completion/error of async operation"
            }
        }
        
        if language in concepts and concept.lower() in concepts[language]:
            explanation = concepts[language][concept.lower()]
            # Store in memory for future reference
            self.memory.add_programming_knowledge(language, concept, explanation)
            return f"📚 {concept}: {explanation}"
        else:
            return f"🤔 I don't have an offline explanation for '{concept}' in {language}. Try asking when online."