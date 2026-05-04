# 🤖 AI Resume Analyzer

A smart web application that analyzes resumes against job descriptions and provides ATS score, skill gap analysis, and improvement suggestions.

---

## 🚀 Features

- 📄 Upload Resume (PDF/DOCX)
- 📊 ATS Score Calculation using Machine Learning
- 🧠 Skill Extraction from Resume
- ⚠️ Missing Skills Detection (based on Job Description)
- 📈 Resume Strength Analysis
- 💡 Actionable Improvement Suggestions
- 🤖 AI Resume Coach (Beta)
- 📥 Downloadable Analysis Report

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Scikit-learn (TF-IDF, Cosine Similarity)  
- PyPDF2  
- python-docx  
- Pandas  

---

## ⚙️ How It Works

1. Upload your resume (PDF or DOCX)  
2. Paste the job description  
3. The system:
   - Extracts text from a resume  
   - Cleans and processes text  
   - Matches resume with job description  
   - Calculates ATS score  
   - Identifies missing skills  
   - Provides improvement suggestions  

---

## ▶️ How to Run Locally

```bash
git clone https://github.com/code2siddhi/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
pip install -r requirements.txt
streamlit run app.py


📊 Output
ATS Score (% match)
Skills matched
Missing skills
Resume strength (Excellent / Good / Needs Work)
Improvement suggestions
Downloadable report
⚠️ Note
A job description is required for accurate analysis
AI chatbot feature is currently in Beta
💡 Key Highlights
Built an end-to-end AI-based resume analysis system
Implemented ATS scoring using TF-IDF and cosine similarity
Designed an interactive Streamlit dashboard
Developed a skill gap detection and improvement system
Integrated AI-based chatbot (Beta)
📌 Use Case

This project helps job seekers:

Understand the resume-job match
Identify missing skills
Improve resume for ATS
🎯 Future Improvements
Improve AI chatbot responses
Add detailed scoring breakdown
Add keyword optimization
Deploy on the cloud
👩‍💻 Author

Siddhi Priya
B.Tech - Electronics & Communication Engineering
Aspiring Software Developer 🚀

⭐ If you like this project

Give it a ⭐ on GitHub!
