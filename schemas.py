from pydantic import BaseModel, Field
from typing import List, Optional

# --- REQUEST SCHEMAS ---
# Jo data user API endpoint par bhejega
# --- REQUEST SCHEMAS ---
class UserProfile(BaseModel):
    name: str = Field(..., example="Tushar")
    skills: List[str] = Field(..., example=["Python", "FastAPI", "MongoDB"])
    experience_level: str = Field(..., example="Beginner")
    
    # CHANGE HERE: 'target_role' ko 'role' kar do kyunki app.py 'role' bhej raha hai
    # Aur default value hata do taaki galti pakdi jaye agar data na aaye
    role: str = Field(..., example="Backend Developer")
# --- RESPONSE SCHEMAS ---
# AI Brain se jo structured data humein chahiye
class CareerAnalysisResponse(BaseModel):
    skill_gap: List[str]
    roadmap: List[str]
    suggested_projects: List[str]
    confidence_score: float

# Database se data nikalne ke liye schema (optional but good)
class UserHistory(BaseModel):
    user_info: UserProfile
    analysis: CareerAnalysisResponse
    created_at: str