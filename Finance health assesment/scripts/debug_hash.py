import sys
import os
sys.path.append(os.getcwd())

from app.core.security import get_password_hash, verify_password

try:
    print("Attempting to hash 'password123'...")
    hash = get_password_hash("password123")
    print(f"Hash success: {hash}")
    
    print("Verifying...")
    valid = verify_password("password123", hash)
    print(f"Verify success: {valid}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
