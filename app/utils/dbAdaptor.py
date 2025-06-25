from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
#from ..auth import hash_password, verify_password
from .. import auth
from fastapi import status

class DBAdaptor:
    
    def __init__(self, uri="mongodb://localhost:27017", db_name="chat_db"):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.users = self.db["users"]
        self.chat_room = self.db["chat_room"]
        self.messages = self.db["messages"]
    def message_dict(self, message):
        return {
            "id": str(message["_id"]),
            "content": message["content"],
            "timestamp": message["timestamp"],
            "user_id": str(message["user_id"]),
            "username": message["username"]
        }

    async def init_room(self):
        room = await self.chat_room.find_one({"room_name": "Global Room"})
        if not room:
            await self.chat_room.insert_one({"room_name": "Global Room"})

    async def sign_up_user(self, username, email, password):
        existing = await self.users.find_one({"email": email})
        if existing:
            return None  # Email already exists
        user = {
            "username": username,
            "email": email,
            "password": auth.hash_password(password)
        }
        result = await self.users.insert_one(user)
        user["_id"] = result.inserted_id
        return self.user_dict(user)

    async def sign_in_user(self, email, password):
        user = await self.users.find_one({"email": email})
        if user and auth.verify_password(password, user["password"]):
            return self.user_dict(user)
        return None
   
    async def post_message(self, content, user_id):
        
        user = await self.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        message = {
            "content": content,
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "username": user["username"],
            "room_id": "global_room"
        }
        result = await self.messages.insert_one(message)
        message["_id"] = result.inserted_id
        return self.message_dict(message)
    
    async def get_all_messages(self):
        cursor = self.messages.find().sort("timestamp", 1)
        messages = []
        async for msg in cursor:
            messages.append(self.message_dict(msg))
        return messages
    
    async def get_user_by_email(self, email: str):
        user = await self.users.find_one({"email": email})
        return user
    
    async def delete_user_message(self, message_id, user_id):
        try:
            message = await self.messages.find_one({"_id": ObjectId(message_id)})
            if not message:
                return False
            if str(message["user_id"]) != user_id:
                return False  # Not the owner
            await self.messages.delete_one({"_id": ObjectId(message_id)})
            return True
        except Exception as e:
            print("Error deleting message:", e)
            return False
    # Add this method to your DBAdaptor class in dbAdaptor.py

    async def get_user_by_id(self, user_id: str):
        """Get user by their ID"""
        try:
            from bson import ObjectId
            user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None    
    def user_dict(self, user):
        return {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }

    def message_dict(self, msg):
        return {
            "id": str(msg["_id"]),
            "content": msg["content"],
            "timestamp": msg["timestamp"],
            "user_id": msg["user_id"],
            "username": msg["username"]
        }
    # Add this method to your DBAdaptor class in dbAdaptor.py

