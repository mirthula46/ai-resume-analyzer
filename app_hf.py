import streamlit as st
import PyPDF2
import requests
import re

# -------------------------------
# 🎨 Advanced UI Styling (NO CHANGE)
# -------------------------------
st.markdown("""
<style>

/* 🌌 Background - Steel Blue Gradient */
.stApp {
    background: linear-gradient(135deg, #2c3e50, #4ca1af);
    color: #ecf0f1;
}

/* 🧠 Animated Title */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

h1 {
    text-align: center;
    color: #ecf0f1;
    animation: float 3s ease-in-out infinite;
    letter-spacing: 1px;
}

/* 🧾 Glass Card */
.card {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.1);
}

/* 🚀 Main Button */
.stButton>button {
    background: linear-gradient(45deg, #4ca1af, #2c3e50);
    color: #ecf0f1;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 17px;
    font-weight: 600;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.04);
    background: linear-gradient(45deg, #2c3e50, #4ca1af);
}

/* 📂 File Uploader Box */
.stFileUploader {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* 📂 Upload Button (Steel Blue) */
.stFileUploader button {
    background: linear-gradient(45deg, #5dade2, #2e86c1) !important;
    color: white !important;
    font-weight: 600;
    border-radius: 8px;
    border: none;
}

/* Hover effect */
.stFileUploader button:hover {
    transform: scale(1.05);
    background: linear-gradient(45deg, #2e86c1, #5dade2) !important;
}

/* 📝 Drag & Drop Text */
.stFileUploader label {
    color: #d6eaf8 !important;
    font-weight: 500;
}

/* 📊 Progress Bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #5dade2, #2e86c1);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🤖 AI Function (Ollama)
# -------------------------------
def ask_ai(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

# -------------------------------
# 📄 Extract PDF text
# -------------------------------
def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# -------------------------------
# 🤖 Agents
# -------------------------------
def resume_agent(resume_text):
    prompt = f"""
    Extract and summarize:
    - Skills
    - Experience
    - Education

    Resume:
    {resume_text}
    """
    return ask_ai(prompt)

def job_agent(job_desc):
    prompt = f"""
    Extract:
    - Required Skills
    - Job Role

    Job Description:
    {job_desc}
    """
    return ask_ai(prompt)

def match_agent(resume, job):
    prompt = f"""
    Compare the resume and job description.

    IMPORTANT:
    - Do NOT make spelling mistakes
    - Do NOT add extra explanation
    - Follow format EXACTLY

    Format:

    Match Score: <number>%
    Candidate Level: Strong / Average / Weak

    Skills Matched:
    - skill 1
    - skill 2

    Missing Skills:
    - skill 1
    - skill 2

    Final Decision:
    2 line explanation only.

    Resume:
    {resume}

    Job:
    {job}
    """
    return ask_ai(prompt)

# -------------------------------
# 📊 Extract Score
# -------------------------------
def extract_score(text):
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 50

# -------------------------------
# 🎯 UI
# -------------------------------
st.title("🚀 Smart AI Resume Analyzer")
st.write("Analyze candidates with AI-powered matching system")

resume_file = st.file_uploader("📄 Upload Resume", type=["pdf"])
job_desc = st.text_area("📝 Paste Job Description")

if st.button("🔍 Analyze Candidate"):
    if resume_file and job_desc:

        with st.spinner("Processing..."):
            resume_text = extract_text(resume_file)
            resume_data = resume_agent(resume_text)
            job_data = job_agent(job_desc)
            result = match_agent(resume_data, job_data)

        score = extract_score(result)

        st.success("Analysis Complete ✅")

        # -------------------------------
        # 📊 Score Bar
        # -------------------------------
        st.subheader("🎯 Match Score")
        st.progress(score / 100)
        st.write(f"### {score}% Match")

        # -------------------------------
        # 📄 Resume Card
        # -------------------------------
        st.subheader("📊 Resume Details")
        st.markdown(f"<div class='card'>{resume_data}</div>", unsafe_allow_html=True)

        # -------------------------------
        # 📌 Job Card
        # -------------------------------
        st.subheader("📌 Job Requirements")
        st.markdown(f"<div class='card'>{job_data}</div>", unsafe_allow_html=True)

        # -------------------------------
        # 🎯 Final Result (CLEANED)
        # -------------------------------
        st.subheader("🎯 Final Result")

        lines = result.split("\n")
        clean_output = ""

        for line in lines:
            line = line.strip()

            if line == "" or "updated version" in line.lower():
                continue

            # Fix typo
            line = line.replace("CanDiaate", "Candidate")

            # Format skills properly
            if "Skills Matched:" in line or "Missing Skills:" in line:
                clean_output += f"• {line}\n"
                continue

            if "," in line:
                parts = line.split(",")
                for part in parts:
                    clean_output += f"• {part.strip()}\n"
            else:
                clean_output += f"• {line}\n"

        st.markdown(f"<div class='card'>{clean_output}</div>", unsafe_allow_html=True)

    else:
        st.warning("Please upload resume and enter job description")