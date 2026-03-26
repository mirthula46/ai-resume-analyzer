# ai-resume-analyzer
Smart AI Resume Analyzer using Streamlit and Ollama
About the Project

This project is a simple web application that helps analyze a candidate’s resume using AI.
It compares the resume with a given job description and gives useful insights like how well the resume matches the job, what skills are missing, and whether the candidate is a good fit.

 What this project can do
 Upload a resume (PDF format)
 Enter a job description
 Analyze the resume using AI
 Show a match score
 Display matched skills
 Highlight missing skills
 Give a final decision (fit or not fit)

 Technologies Used
Python
Streamlit (for building the web interface)
Ollama – TinyLlama model (for AI processing)
PyPDF2 (to read PDF files)
Requests (for API communication)

How the system works
The user uploads a resume in PDF format
The user enters the job description
The system extracts text from the resume
AI analyzes both the resume and job description
Finally, it shows:
Match score
Skills that match
Skills that are missing
Final hiring suggestion

How to run this project
Step 1: Install required packages
pip install streamlit PyPDF2 requests
Step 2: Start the AI model
ollama run tinyllama
Step 3: Run the application
streamlit run app_hf.py

 Output
Shows match score using a progress bar
Displays resume content and job description
Gives a clear and structured result

 Future Improvements
Use more advanced AI models like Llama3 or Phi-3
Add user login system
Improve UI design and animations
Deploy the project online
