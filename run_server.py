#!/usr/bin/env python
"""
Simple script to run the Django application with uvicorn.
"""
import os
import sys

def main():
    """Run the application with uvicorn."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
    
    # Check if uvicorn is installed
    try:
        import uvicorn
    except ImportError:
        print("Uvicorn is not installed. Please install it with:")
        print("pip install uvicorn")
        sys.exit(1)
    
    # Pre-flight check for static files
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'staticfiles')):
        print("Collecting static files...")
        os.system("python manage.py collectstatic --noinput")
    
    # Run the application
    uvicorn.run(
        "taskmanager.asgi:application",
        host="127.0.0.1",
        port=8002,  # Changed from 8001 to 8002
        reload=True  # Auto-reload on code changes
    )

if __name__ == "__main__":
    main() 