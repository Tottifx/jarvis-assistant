#!/bin/bash

echo "�� JARVIS AI Assistant Setup"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "jarvis_env" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv jarvis_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source jarvis_env/bin/activate

# Install requirements
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/logs data/temp

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your DeepSeek API key"
fi

# Test basic functionality
echo "🧪 Testing basic imports..."
python -c "
import speech_recognition, pyttsx3, requests
print('✅ All core packages installed successfully!')
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add your DeepSeek API key: DEEPSEEK_API_KEY=your_key_here"
echo "3. Activate environment: source jarvis_env/bin/activate"
echo "4. Run JARVIS: python main.py"
echo ""
echo "💡 For offline mode, set OFFLINE_MODE=true in .env file"
