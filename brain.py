import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
# Purana 'class CareerAnalysis' hata do aur ye dalo:
from schemas import CareerAnalysisResponse
from config import settings

# Ab tum direct 'settings.AI_MODEL' aur 'settings.OPENAI_API_KEY' use kar sakte ho

# ... inside class ...


# Environment variables load karo
load_dotenv()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# --- AI RESPONSE SCHEMA ---
# Ye define karta hai ki GPT se humein exactly kya-kya chahiye
# class CareerAnalysis(BaseModel):
#     skill_gap: List[str]      # Kaunsi skills missing hain
#     roadmap: List[str]        # Agle steps kya hone chahiye
#     suggested_projects: List[str] # Practice ke liye projects
#     confidence_score: float   # 0 to 1 ke beech mein ranking

class CareerBrain:
    def __init__(self):
        self.model = settings.AI_MODEL

    async def analyze_user_profile(self, name: str, skills: List[str], target_role: str):
        """
        User ki skills aur target role ko analyze karke roadmap deta hai.
        """
        print(f"[Brain Log] Analyzing {name}'s profile for {target_role}...")

        # Sateek Prompt Engineering
        # prompt = f"""
        # You are a Senior Technical Career Coach. Analyze the following profile:
        # Name: {name}
        # Current Skills: {", ".join(skills)}
        # Target Role: {target_role}

        # Provide a structured career analysis including:
        # 1. Skill Gaps (What they need to learn to reach the target role).
        # 2. A step-by-step 4-week roadmap.
        # 3. Two project ideas to build their portfolio.
        # 4. A confidence score (0.0 to 1.0) based on their current skills vs target role.

        # Return the response in a clean JSON format.
        # """
        
        prompt = f"""
        You are a Senior Technical Career Coach. Analyze this profile:
        Name: {name}, Target Role: {target_role}, Current Skills: {", ".join(skills)}
        
        INSTRUCTIONS:
        1. "skill_gap": List 3-4 specific technical topics.
        2. "roadmap": This MUST be a list of 4 strings. Each string should contain 3-4 bullet points separated by a newline character (\\n). 
           Example: "• Learn FastAPI Basics\\n• Understand Pydantic Schemas\\n• Build 2 CRUD APIs"
        3. "suggested_projects": 2 Projects with NAME and a 2-line Execution Plan.
        4. "confidence_score": Float (0.0 to 1.0).
        
        Return ONLY valid JSON.
        """
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a career advisor that outputs only JSON."},
                          {"role": "user", "content": prompt}],
                response_format={"type": "json_object"} # Ensure JSON output
            )

            # GPT ka raw response
            raw_ai_data = response.choices[0].message.content
            return raw_ai_data

        except Exception as e:
            print(f"[Error] Brain execution fail ho gayi: {e}")
            return None