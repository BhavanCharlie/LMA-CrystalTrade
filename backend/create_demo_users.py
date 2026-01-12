#!/usr/bin/env python3
"""
Quick script to create demo users
"""
from database import get_db, init_db
from models import User
import bcrypt

def create_demo_users():
    """Create demo users if they don't exist"""
    print("Creating demo users...")
    
    # Initialize database
    init_db()
    
    db = next(get_db())
    try:
        demo_users = [
            {
                "id": "demo-user-001",
                "email": "demo@crystaltrade.com",
                "username": "demo",
                "password": "demo123",
                "full_name": "Demo User",
                "is_admin": False,
            },
            {
                "id": "admin-user-001",
                "email": "admin@crystaltrade.com",
                "username": "admin",
                "password": "admin123",
                "full_name": "Admin User",
                "is_admin": True,
            },
        ]
        
        for user_data in demo_users:
            existing_user = db.query(User).filter(
                (User.email == user_data["email"]) | (User.username == user_data["username"])
            ).first()
            
            if existing_user:
                # Update password if user exists (in case it was created incorrectly)
                print(f"  Updating existing user: {user_data['username']}")
                hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                existing_user.hashed_password = hashed_password
                existing_user.is_active = True
            else:
                # Create new user
                hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user = User(
                    id=user_data["id"],
                    email=user_data["email"],
                    username=user_data["username"],
                    hashed_password=hashed_password,
                    full_name=user_data["full_name"],
                    is_active=True,
                    is_admin=user_data["is_admin"],
                )
                db.add(user)
                print(f"  ✓ Created user: {user_data['username']} ({user_data['email']})")
        
        db.commit()
        print("\n✅ Demo users ready!")
        print("\n📋 Demo Credentials:")
        print("  Regular User:")
        print("    Username: demo")
        print("    Password: demo123")
        print("  Admin User:")
        print("    Username: admin")
        print("    Password: admin123")
        
    except Exception as e:
        print(f"❌ Error creating demo users: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_users()
