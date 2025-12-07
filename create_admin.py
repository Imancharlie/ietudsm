"""
Script to create a superuser/admin account
Run: python create_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iet_system.settings')
django.setup()

from accounts.models import User

def create_admin():
    print("=" * 50)
    print("Create IET System Admin Account")
    print("=" * 50)
    
    email = input("\nEnter email address: ")
    password = input("Enter password: ")
    
    if User.objects.filter(email=email).exists():
        print(f"\n❌ User with email '{email}' already exists!")
        return
    
    try:
        user = User.objects.create_superuser(
            username=email,
            email=email,
            password=password,
            is_staff=True
        )
        print(f"\n✅ Superuser created successfully!")
        print(f"   Email: {email}")
        print(f"\nYou can now login at: http://127.0.0.1:8000/accounts/login/")
    except Exception as e:
        print(f"\n❌ Error creating superuser: {e}")

if __name__ == '__main__':
    create_admin()



