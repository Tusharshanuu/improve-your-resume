from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from datetime import datetime
import certifi

class CareerDatabase:
    def __init__(self):
        # String ko clean karna zaroori hai
        uri = settings.MONGO_URL.strip() 
        try:
            self.client = AsyncIOMotorClient(uri, tlsCAFile=certifi.where())
            self.db = self.client[settings.DATABASE_NAME]
            # Collection ko yahan initialize karna compulsory hai
            self.collection = self.db.user_reports
            print(f"[DB Log] Successfully connected to Database: {settings.DATABASE_NAME}")
        except Exception as e:
            print(f"[Fatal Error] Database initialize nahi ho paya: {e}")

    # async def save_analysis(self, user_data: dict, ai_analysis: dict):
     # database.py mein save_analysis function ke andar
    async def save_analysis(self, user_data: dict, analysis: dict):
    # Agar tum user_data se role nikal rahe ho, toh check karo key kya hai
        role = user_data.get("role") or user_data.get("target_role") # Dono check kar lo safety ke liye
    
    # Baaki saving logic...
        # Check karo ki collection bani hai ya nahi
        if not hasattr(self, 'collection'):
            print("[Error] Database connection missing. Save cancel.")
            return False
            
        try:
            document = {
                "user_info": user_data,
                "analysis": ai_analysis,
                "created_at": datetime.utcnow().isoformat()
            }
            result = await self.collection.insert_one(document)
            print(f"[DB Log] Data saved! ID: {result.inserted_id}")
            return True
        except Exception as e:
            print(f"[Error] Save karte waqt issue: {e}")
            return False