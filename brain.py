from openai import OpenAI
from config import settings
from dotenv import load_dotenv
from typing import List

# Environment variables load karo
load_dotenv()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class CareerBrain:
    def __init__(self):
        self.model = settings.AI_MODEL

    async def analyze_user_profile(self, name: str, skills: str, target_role: str):
        """
        User ki skills aur target role ko analyze karke roadmap deta hai.
        """
        print(f"[Brain Log] Analyzing {name}'s profile for {target_role}...")

        # --- SATEEK PROMPT ---
        # brain.py mein prompt ko aise update karo
        # prompt = f"""
        # You are a World-Class Career Consultant. Your expertise spans across Technical and Non-Technical industries (Marketing, Finance, Arts, Management, etc.).
        
        # ### YOUR TASK:
        # Generate a professional 4-week roadmap specifically for the Target Role: '{target_role}'.
        
        # ### STRICT RULES:
        # 1. **Domain Relevance**: If the role is '{target_role}', ONLY suggest skills and topics related to that field. 
        #    - Example: If role is 'Digital Marketing', focus on SEO, SEM, and Content.
        #    - Example: If role is 'HR Manager', focus on Recruitment, Payroll, and Labour Laws.
        # 2. **NO TECH BIAS**: Do NOT mention Programming, AI, or Math UNLESS the '{target_role}' is a technical role.
        # 3. **Skill Gap**: Compare the 'Current Skills' ({skills}) with the standard requirements of '{target_role}'. Identify what is missing for THIS SPECIFIC role.
        # 4. **Day-wise Plan**: Provide a logical, 4-week learning path (Day 1 to 7 each week).
        
        # ### OUTPUT FORMAT (Valid JSON):
        # - "weaknesses": String (Gaps specific to {target_role})
        # - "roadmap": Dictionary (Week 1-4 with Day 1-7 breakdown)
        # - "resources": List of 3-4 clickable URLs (YouTube, Courses, or Articles) relevant to {target_role}.
        # """
        # --- SATEEK PROMPT ---
        prompt = f"""
        You are a World-Class Career Consultant... (baaki purana text)
        
        ### OUTPUT FORMAT (Valid JSON):
        - "top_skills": List of 3-4 most important keywords/tools for {target_role}  <-- YE LINE ADD KARNI HAI
        - "weaknesses": String (Gaps specific to {target_role})
        - "roadmap": Dictionary (Week 1-4 with Day 1-7 breakdown)
        - "resources": List of 3-4 clickable URLs relevant to {target_role}.
        """
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a Neutral Career Consultant. "
                            "NEVER assume every user wants to learn AI. "
                            "If the target role is non-technical (like HR, Sales, Chef, etc.), "
                            "DO NOT mention Python, Machine Learning, or Math. "
                            "Output ONLY valid JSON."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            # ... baaki ka parsing code
            # GPT ka raw response
            raw_ai_data = response.choices[0].message.content
            import json
            return json.loads(raw_ai_data) # String ko Dictionary mein badal kar bhej rahe hain

        except Exception as e:
            print(f"[Error] Brain execution fail ho gayi: {e}")
            return {
                "weaknesses": "Analysis failed.",
                "roadmap": "Could not generate roadmap.",
                "resources": "No resources found."
            }