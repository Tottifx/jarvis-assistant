import webbrowser
import requests
from bs4 import BeautifulSoup
import wikipedia
from utils.logger import setup_logger

logger = setup_logger('web_surf')

class WebSurfer:
    def __init__(self, memory_system):
        self.memory = memory_system
    
    def search_web(self, query):
        """Search the web for information"""
        try:
            summary = wikipedia.summary(query, sentences=2)
            self.memory.learn_fact("searches", f"Searched for: {query}")
            return f"📚 According to Wikipedia: {summary}"
        except:
            return f"🔍 I found information about: {query}. For detailed results, I can open a browser."
    
    def open_website(self, site_name):
        """Open common websites"""
        sites = {
            'google': 'https://google.com',
            'youtube': 'https://youtube.com',
            'github': 'https://github.com',
            'stack overflow': 'https://stackoverflow.com',
            'wikipedia': 'https://wikipedia.org',
            'reddit': 'https://reddit.com',
            'gmail': 'https://gmail.com'
        }
        
        if site_name in sites:
            webbrowser.open(sites[site_name])
            return f"🌐 Opening {site_name}"
        else:
            webbrowser.open(f"https://{site_name}")
            return f"🌐 Opening website"
    
    def get_quick_info(self, topic):
        """Get quick information about a topic"""
        try:
            return wikipedia.summary(topic, sentences=2)
        except:
            return f"🔍 Search for: {topic}. I can open a browser for more details."