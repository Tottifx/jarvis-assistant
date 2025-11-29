import re
import os

def clean_filename(filename):
    """Clean filename to be filesystem-safe"""
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

def get_file_extension(language):
    """Get file extension for programming language"""
    extensions = {
        'python': '.py',
        'javascript': '.js',
        'java': '.java',
        'cpp': '.cpp',
        'c++': '.cpp',
        'c': '.c'
    }
    return extensions.get(language.lower(), '.txt')

def format_code_block(code, language='python'):
    """Format code for display"""
    return f"```{language}\n{code}\n```"