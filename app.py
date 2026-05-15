import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(page_title="Career Architect AI", page_icon="🚀", layout="wide")

# Backend URL (Render Live Link)
BACKEND_URL = "https://improve-your-resume.onrender.com"
# BACKEND_URL = "http://127.0.0.1:8000"
st.title("🚀 Career Architect AI")
st.markdown("### Build your professional career roadmap")

# --- SIDEBAR: User Input ---
st.sidebar.header("User Profile")
name = st.sidebar.text_input("Full Name", placeholder="Enter Your Name")
target_role = st.sidebar.text_input("Target Role", placeholder="e.g. AI Engineer,Graphic design")
exp_level = st.sidebar.selectbox("Experience Level", ["Beginner", "Intermediate", "Pro"])

# Skills input
skills_raw = st.sidebar.text_area("Skills (Comma separated)", placeholder="PYTHON, JAVA, etc.")

# --- MAIN SECTION ---
if st.button("Generate My Roadmap"):
    # Basic Validation: Name, Role aur Skills hone chahiye
    if name and target_role and skills_raw:
        with st.spinner("AI is deep-scanning your profile..."):
            try:
                # Backend ke liye data taiyar karo
                # Note: 'role' variable backend ke 'data.get("role")' se match karega
                # skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
                skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
                payload = {
                    "name": name,
                    "role": target_role, 
                    "skills": skills_list,
                    "experience_level": exp_level
                }
                
                # FastAPI Backend ko call karo
                # response = requests.post(f"{BACKEND_URL}/analyze-skills", json=payload)
                response = requests.post(f"{BACKEND_URL}/analyze-skills", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    analysis = result.get("analysis", {})
                    
                    st.balloons()
                    st.success(f"Congratulations {name}! Your deep roadmap is ready below.")

                    # --- NAYA SECTION: TOP SKILLS (BADE CARDS) ---
                    top_skills = analysis.get("top_skills", [])
                    if top_skills:
                        st.subheader("🔥 Key Skills to Master")
                        # 4 columns banate hain taaki cards side-by-side aayein
                        skill_cols = st.columns(len(top_skills))
                        for i, skill in enumerate(top_skills):
                            with skill_cols[i]:
                                st.markdown(
                                    f"""
                                    <div style="
                                        background-color: #ff4b4b; 
                                        color: white; 
                                        padding: 20px; 
                                        border-radius: 15px; 
                                        text-align: center; 
                                        font-weight: bold; 
                                        font-size: 22px;
                                        box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
                                        border: 2px solid #ffffff;
                                    ">
                                        {skill}
                                    </div>
                                    """, 
                                    unsafe_allow_html=True
                                )
                        st.write("") # Thoda space dene ke liye
                    # ---------------------------------------------

                    # --- Section 1: Skill Gaps (Weaknesses) ---
                    st.subheader("🎯 Skill Gaps & Weaknesses")
                    weak_text = analysis.get("weaknesses", "No specific gaps identified.")
                    st.error(weak_text)
                    
                    st.divider()
                    # ... baaki ka roadmap code

                    # --- Section 2: Detailed Roadmap ---
                   # app.py mein jahan roadmap display kar rahe ho
                  # app.py update
                    st.subheader("📅 Detailed Day-by-Day Roadmap")
                    roadmap_data = analysis.get("roadmap", {})
                    
                    if isinstance(roadmap_data, dict):
                        for week, days in roadmap_data.items():
                            with st.expander(f"🚀 {week}"):
                                if isinstance(days, dict):
                                    for day, task in days.items():
                                        # Har day ko bold aur task ko clean dikhayega
                                        st.markdown(f"**{day}:** {task}")
                                else:
                                    st.write(days) # Backup agar format change ho

                    # --- Section 3: Free Resources ---
                    st.subheader("📚 Top Free Resources to Learn")
                    # Humne brain.py mein 'resources' key rakhi hai
                    resource_links = analysis.get("resources", "No specific links found.")
                    st.success(resource_links)

                else:
                    st.error(f"Backend Issue: {response.status_code}")
                    st.write("Server response:", response.text)

            except Exception as e:
                st.error("Connection Fail! Check karo ki server online hai?")
                st.exception(e)
    else:
        st.warning("Please fill all details (Name, Role, and Skills) in the sidebar!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Tushar | AI Engineering 2026")