#!/usr/bin/env python3
import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'python-multipart', 
        'merkletools', 'cryptography'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Please install with: pip install " + " ".join(missing))
        return False
    return True

def main():
    print("🔐 Starting zk-creds Demo")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    if os.path.exists(backend_dir):
        os.chdir(backend_dir)
    
    print("Starting server...")
    print("Open your browser to: http://localhost:8000")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    # Start the server
    subprocess.run([sys.executable, 'main.py'])

if __name__ == "__main__":
    main()