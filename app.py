import streamlit as st
from utils import extract_resume_text, clean_text, extract_skills, calculate_similarity

st.title("AI Resume Analyzer")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

# Job description input
job_description = st.text_area("Paste Job Description")

# Show message if nothing entered
if uploaded_file is None or job_description == "":
    st.info("Please upload resume and paste job description to continue.")

# Process when both inputs are given
if uploaded_file is not None and job_description != "":
    text = extract_resume_text(uploaded_file)

    if text == "":
        st.error("Unsupported file format")
    else:
        cleaned_resume = clean_text(text)
        cleaned_jd = clean_text(job_description)

        skills = extract_skills(cleaned_resume)
        score = calculate_similarity(cleaned_resume, cleaned_jd)

        st.subheader("Extracted Skills:")
        st.write(skills)

        st.subheader("ATS Score:")
        st.progress(int(score))
        st.write(f"{score}% match")