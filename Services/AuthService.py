from db.UserDbContext import UserDb
from secrets import token_bytes
import hashlib, hmac, base64


class Authentication:
    def __init__(self):
        self.users = {}
        
    

    def register(self, username, password):
        if username in self.users:
            return "Username already exists."
        self.users[username] = password
        return "User registered successfully."

    def login(self, username, password):
        if username not in self.users:
            return "User not found."
        if self.users[username] != password:
            return "Incorrect password."
        return "Login successful."

    def logout(self, username):
        if username not in self.users:
            return "User not found."
        return f"{username} logged out successfully."
    
    def hash_password(self, password: str) -> tuple[str, str]:
        # sourcery skip: avoid-builtin-shadow
        salt = token_bytes(16)
        hash = hashlib.pbkdf2_hmac('sha256', password.encode("utf-8"), salt, 100_000)
        return base64.b64encode(salt).decode('utf-8'), base64.b64encode(hash).decode('utf-8')
    
    def verify_password(self, password: str, salt: str, hash: str) -> bool:
        decoded_salt = base64.b64decode(salt)
        decoded_hash = base64.b64decode(hash)
        new_hash = hashlib.pbkdf2_hmac('sha256', password.encode("utf-8"), decoded_salt, 100_000)
        return hmac.compare_digest(new_hash, decoded_hash)
    
