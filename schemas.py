from pydantic import BaseModel, Field
from typing import List, Optional

# --- REQUEST SCHEMAS ---
# Jo data user API endpoint par bhejega
class UserProfile(BaseModel):
    name: str = Field(..., example="Tushar")
    skills: List[str] = Field(..., example=["Python", "FastAPI", "MongoDB"])
    experience_level: str = Field(..., example="Beginner")
    target_role: Optional[str] = Field(default="AI Engineer", example="ML Engineer")

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