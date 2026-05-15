from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# 1. Sabse pehle imports aur initialization
from brain import CareerBrain
from database import CareerDatabase
# Purana 'class UserProfile' hata do aur ye dalo:
from schemas import UserProfile

app = FastAPI(title="Career Architect AI", version="1.0.0")

# Agents initialize karo
brain_agent = CareerBrain()
db_agent = CareerDatabase()

# 2. SCHEMAS
# class UserProfile(BaseModel):
#     name: str
#     skills: List[str]
#     experience_level: str 
#     target_role: Optional[str] = "AI Engineer"

# 3. ROUTES

@app.get("/")
def home():

    return {"message": "Welcome to Career Architect AI! Your roadmap starts here."}

@app.post("/analyze-skills")
async def analyze_skills(profile: UserProfile):
    try:
        print(f"DEBUG: Data Received -> {profile.model_dump()}") # Ye terminal mein poora data dikhayega
        
        # Step 1: Brain call
        ai_response = await brain_agent.analyze_user_profile(
            name=profile.name, 
            skills=profile.skills, 
            target_role=profile.role 
        )
        
        # Step 2: Database call (Yahan error ho sakta hai)
        await db_agent.save_analysis(profile.model_dump(), ai_response)
        
        return {"status": "Success", "analysis": ai_response}

    except Exception as e:
        import traceback
        print(traceback.format_exc()) # Ye terminal mein batayega ki error kaunsi line par hai
        raise HTTPException(status_code=500, detail=str(e))
        
        # ... baaki code
        
        # Step 2: Database mein save karo
        await db_agent.save_analysis(profile.model_dump(), ai_response)
        
        # return {
        #     "status": "Success",
        #     "user": profile.name,
        #     "analysis": ai_response
        # }
        return {
            "status": "Success",
            "analysis": ai_response # Ye wahi response hai jo brain.py se aaya
}

    except Exception as e:
        print(f"Error occurred: {e}") # Debugging ke liye
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "System is up and running"}