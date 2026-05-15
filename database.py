from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from datetime import datetime
import certifi

class CareerDatabase:
    def __init__(self):
        # 1. MongoDB Connection string clean aur initialize karna
        uri = settings.MONGO_URL.strip() 
        try:
            # TLS/SSL certificate fix ke saath connection
            self.client = AsyncIOMotorClient(uri, tlsCAFile=certifi.where())
            self.db = self.client[settings.DATABASE_NAME]
            
            # Collection initialize karna
            self.collection = self.db.user_reports
            print(f"[DB Log] Successfully connected to Database: {settings.DATABASE_NAME}")
        except Exception as e:
            print(f"[Fatal Error] Database initialize nahi ho paya: {e}")

    async def save_analysis(self, user_data: dict, analysis: dict):
        """
        User ki information aur AI ka roadmap database mein save karta hai.
        """
        # 1. Connection safety check
        if not hasattr(self, 'collection'):
            print("[Error] Database connection missing. Save cancel.")
            return False
            
        try:
            # 2. Document taiyar karna (Indentation check: 8 spaces from margin)
            document = {
                "user_info": user_data,
                "analysis": analysis,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # 3. Database mein insert command
            result = await self.collection.insert_one(document)
            
            print(f"[DB Log] Data saved successfully! ID: {result.inserted_id}")
            return True
            
        except Exception as e:
            print(f"[Error] Save karte waqt issue aaya: {e}")
            return False