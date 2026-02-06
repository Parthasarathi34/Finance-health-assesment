import sys
import os
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def verify():
    db = SessionLocal()
    print("Database connection established.")
    
    # Check if test user exists
    user = db.query(User).filter(User.email == "test@example.com").first()
    if not user:
        print("Creating test user...")
        user = User(
            email="test@example.com",
            password_hash=get_password_hash("password123"),
            full_name="Test User",
            is_active=True
        )
        db.add(user)
        db.commit()
        print("Test user created.")
    else:
        print("Test user already exists.")
        
    print(f"User ID: {user.id}")
    db.close()
    print("Verification successful.")

if __name__ == "__main__":
    verify()
