"""
Setup script for IET Membership System
Run this script to initialize the database and create a superuser
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iet_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

def main():
    print("=" * 50)
    print("IET Membership System - Setup")
    print("=" * 50)
    
    # Run migrations
    print("\n1. Running migrations...")
    call_command('makemigrations')
    call_command('migrate')
    print("✓ Migrations completed")
    
    # Create superuser
    print("\n2. Creating superuser...")
    print("Please enter the following details:")
    
    email = input("Email: ")
    password = input("Password: ")
    
    if User.objects.filter(email=email).exists():
        print(f"✗ User with email {email} already exists")
    else:
        User.objects.create_superuser(
            username=email,
            email=email,
            password=password,
            is_staff=True
        )
        print(f"✓ Superuser created: {email}")
    
    print("\n" + "=" * 50)
    print("Setup completed!")
    print("=" * 50)
    print("\nTo start the server, run:")
    print("  python manage.py runserver")
    print("\nThen visit:")
    print("  http://127.0.0.1:8000/")

if __name__ == '__main__':
    main()




