#!/usr/bin/env python
"""
Script to collect static files for Django deployment.
"""
import os
import subprocess

if __name__ == "__main__":
    # Ensure STATIC_ROOT directory exists
    os.makedirs('staticfiles', exist_ok=True)
    
    # Run collectstatic command
    subprocess.call(['python', 'manage.py', 'collectstatic', '--noinput'])
    
    # Create a .gitkeep file in staticfiles directory
    with open('staticfiles/.gitkeep', 'w') as f:
        f.write('# This file ensures the staticfiles directory is included in Git\n')
    
    print("Static files collected successfully!") 