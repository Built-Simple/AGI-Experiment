#!/usr/bin/env python3
"""
setup_experiments.py
One-time setup for AGI impossibility experiments
"""

import os
import subprocess
import sys

def setup():
    print("🔧 Setting up AGI Impossibility Experiments")
    
    # Install requirements
    requirements = [
        'anthropic',
        'openai',
        'matplotlib',
        'numpy',
        'python-dotenv'
    ]
    
    print("📦 Installing requirements...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + requirements)
    
    # Create .env file
    if not os.path.exists('.env'):
        print("\n⚠️  Create a .env file with:")
        print("ANTHROPIC_API_KEY=your-key-here")
        print("OPENAI_API_KEY=your-key-here (optional)")
        
        with open('.env', 'w') as f:
            f.write("# Add your API keys here\n")
            f.write("ANTHROPIC_API_KEY=\n")
            f.write("OPENAI_API_KEY=\n")
    
    print("\n✅ Setup complete! Edit .env with your API keys")

if __name__ == "__main__":
    setup()