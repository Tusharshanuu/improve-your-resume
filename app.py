import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(page_title="Career Architect AI", page_icon="🚀", layout="wide")

# Backend URL (FastAPI ka address)
# BACKEND_URL = "http://127.0.0.1:8000"
BACKEND_URL = "https://improve-your-resume.onrender.com"

st.title("🚀 Career Architect AI")
st.markdown("### Build your professional career roadmap")

# --- SIDEBAR: User Input ---
st.sidebar.header("User Profile")
name = st.sidebar.text_input("Full Name", placeholder="Enter Your Name")
target_role = st.sidebar.text_input("Target Role", placeholder="e.g. AI Engineer")
exp_level = st.sidebar.selectbox("Experience Level", ["Beginner", "Intermediate", "Pro"])

# Skills input (Comma separated)
skills_raw = st.sidebar.text_area("Skills (Comma separated)", placeholder="Python, FastAPI, MongoDB")

# --- MAIN SECTION ---
if st.sidebar.button("Generate My Roadmap"):
    if not name or not skills_raw:
        st.error("Please Enter Your Name and Skills")
    else:
        # Skills ko list mein badlo
        skills_list = [s.strip() for s in skills_raw.split(",")]
        
        # FastAPI ke liye data taiyar karo
        payload = {
            "name": name,
            "skills": skills_list,
            "experience_level": exp_level,
            "target_role": target_role if target_role else "AI Engineer"
        }

        with st.spinner("Please Wait you Roadmap is Generating"):
            try:
                # 1. FastAPI Backend ko call karo
                response = requests.post(f"{BACKEND_URL}/analyze-skills", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    ai_raw = result.get("analysis")

                    # 1. AI Response ko Parse karo (Agar string hai toh JSON mein badlo)
                    try:
                        if isinstance(ai_raw, str):
                            analysis = json.loads(ai_raw)
                        else:
                            analysis = ai_raw
                    except Exception as parse_error:
                        st.error(" Sorry! Format is wrong")
                        st.write("Raw Data:", ai_raw)
                        analysis = {}

                    # 2. UI Par Display Karo
                    if analysis:
                        st.success(f"Congratulations {name}! Your Roadmap is ready in below")

                        # --- Section 1: Skill Gaps ---
                        st.subheader("🎯 Skill Gaps")
                        gaps = analysis.get("skill_gap", [])
                        if gaps:
                            cols = st.columns(len(gaps))
                            for i, gap in enumerate(gaps):
                                cols[i].error(f"**{gap}**")
                        else:
                            st.write("You are Pro No difference in your skill")

                        st.divider()

                        # --- Section 2: Roadmap ---
                        st.subheader("📅 4-Week Roadmap")
                        roadmap = analysis.get("roadmap", [])
                        if roadmap:
                            for i, step in enumerate(roadmap):
                                with st.expander(f"Week {i+1} Plan", expanded=True):
                                    st.markdown(step)
                        else:
                            st.warning("Roadmap is not generating. Please check your Prompt.")

                        st.divider()

                        # --- Section 3: Projects ---
                        st.subheader("🛠️ Suggested Projects")
                        projects = analysis.get("suggested_projects", [])
                        if projects:
                            for project in projects:
                                st.warning(f"🚀 {project}")
                        else:
                            st.info("Projects ki list khali hai.")
                else:
                    st.error(f"Backend Issue: {response.status_code}")
                    st.write(response.text)

                    

            except Exception as e:
                st.error("Connection Fail! Check karo ki 'uvicorn main:app' chal raha hai?")
                st.exception(e)

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Tushar | AI Engineering 2026")