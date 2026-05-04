import streamlit as st
import pandas as pd
from utils import extract_resume_text, clean_text, extract_skills, calculate_similarity, get_missing_skills, get_matched_keywords
from suggestions import get_improvement_suggestions, calculate_resume_strength, generate_chatbot_response

# Set wide layout and professional title
st.set_page_config(page_title="AI Resume Analyzer", layout="wide", page_icon="📄")

st.title("🤖 Professional AI Resume Analyzer")
st.markdown("Optimize your resume for Applicant Tracking Systems (ATS) and get actionable feedback.")

with st.expander("ℹ️ About This App & How to Use", expanded=False):
    st.markdown("""
    **🎯 What does this app do?**
    This AI-powered tool compares your resume against a specific job description to determine your Applicant Tracking System (ATS) compatibility.
    
    **⚙️ How does the ATS score work?**
    The ATS score is calculated using NLP (TF-IDF and Cosine Similarity). It measures the textual overlap and relevance of keywords between your resume and the job requirements.
    
    **📈 How to improve your resume?**
    Review the 'Missing Skills' and 'Improvement Suggestions' sections below. Tailoring your resume with action verbs, measurable metrics, and exact keywords from the job description will drastically increase your chances of passing an ATS.
    
    ---
    ### 📖 How to Use:
    1. 📄 **Upload** your resume (PDF or DOCX) in the sidebar.
    2. 📋 **Paste** the target job description in the sidebar text area.
    3. 🚀 **View** your instant results, click on the metrics, explore the tabs, and download your final report!
    """)

# Sidebar for Inputs
with st.sidebar:
    st.header("Upload Details")
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste Job Description", height=200)
    
    st.markdown("---")
    st.markdown("💡 *Tip: Ensure the job description is detailed for better accuracy.*")

# Show message if nothing entered
if uploaded_file is None or job_description == "":
    st.info("👈 Please upload your resume and paste the job description in the sidebar to get started.")

# Process when both inputs are given
if uploaded_file is not None and job_description != "":
    with st.spinner("Analyzing your resume..."):
        text = extract_resume_text(uploaded_file)

        if text == "":
            st.error("Unsupported file format")
        else:
            # 1. Text processing
            cleaned_resume = clean_text(text)
            cleaned_jd = clean_text(job_description)

            # 2. Extract Data
            resume_skills = extract_skills(cleaned_resume)
            ats_score = calculate_similarity(cleaned_resume, cleaned_jd)
            # Use cleaned_jd instead of raw job_description to fix missing skills bug
            missing_skills = get_missing_skills(resume_skills, cleaned_jd)
            matched_keywords = get_matched_keywords(cleaned_resume, cleaned_jd)
            
            # 3. Suggestions & Strength
            suggestions = get_improvement_suggestions(cleaned_resume)
            strength_score, strength_label, strength_color = calculate_resume_strength(ats_score, suggestions)

            # Job Description Validation
            if len(cleaned_jd.split()) < 30:
                st.warning("⚠️ Job description is too short for highly accurate analysis. Please provide more details if possible.")
            else:
                st.success("Analysis Complete!")
            
            # --- DASHBOARD METRICS ---
            st.markdown("### 📊 Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Top Level ATS Score
                st.metric(label="ATS Score Match", value=f"{ats_score}%")
                st.progress(min(1.0, int(ats_score) / 100))
                # ATS Score Interpretation
                if ats_score >= 80:
                    st.caption("🟢 Strong")
                elif ats_score >= 60:
                    st.caption("🟡 Moderate")
                else:
                    st.caption("🔴 Needs improvement")
                
            with col2:
                # Resume Strength
                st.metric(label="Resume Strength", value=strength_label)
                st.progress(min(1.0, int(strength_score) / 100))
                # Interactive Resume Strength
                if "Needs Work" in strength_label:
                    with st.popover("🚨 See Why"):
                        st.markdown("**Critical issues found!** Your resume might lack measurable achievements or action verbs. Please navigate to the **Improvement Suggestions** tab for a detailed breakdown.")
                elif "Good" in strength_label:
                    with st.popover("💡 See How to Improve"):
                        st.markdown("You are on the right track! Review the **Improvement Suggestions** tab to see how you can bump this up to Excellent.")
                
            with col3:
                # Found skills count
                st.metric(label="Skills Matched", value=len(resume_skills))
                st.markdown("[🔍 View Matched Skills](#skills-found-in-resume)")
                
            with col4:
                # Missing skills count
                st.metric(label="Missing Skills", value=len(missing_skills), delta=-len(missing_skills), delta_color="inverse")
                st.markdown("[🚨 View Missing Skills](#skills-missing-from-resume)")

            # --- DETAILED ANALYSIS SECTIONS ---
            st.markdown("---")
            
            # Using Tabs for detailed breakdowns
            # Using Tabs for detailed breakdowns
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Matched Skills", "⚠️ Missing Skills", "🔑 Matched Keywords", "📈 Improvement Suggestions", "📊 Skill Analysis Chart"])
            
            with tab1:
                st.subheader("Skills Found in Resume")
                if resume_skills:
                    skills_html = " ".join([f"<span style='background-color:#e6f2ff; color:#005cbf; padding: 5px 10px; border-radius: 15px; margin: 5px; display: inline-block;'>{skill}</span>" for skill in resume_skills])
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.warning("No standard tech skills detected.")
                    
            with tab2:
                st.subheader("Skills Missing from Resume")
                if missing_skills:
                    missing_html = " ".join([f"<span style='background-color:#ffe6e6; color:#cc0000; padding: 5px 10px; border-radius: 15px; margin: 5px; display: inline-block;'>{skill}</span>" for skill in missing_skills])
                    st.markdown(missing_html, unsafe_allow_html=True)
                else:
                    st.success("Great job! You have all the hard skills listed in the job description.")
            
            with tab3:
                st.subheader("Top Matched Keywords")
                if matched_keywords:
                    st.write("These are the most common significant words shared between your resume and the job description:")
                    keywords_html = " ".join([f"<span style='background-color:#e8f5e9; color:#2e7d32; padding: 5px 10px; border-radius: 15px; margin: 5px; display: inline-block;'>{kw}</span>" for kw in matched_keywords])
                    st.markdown(keywords_html, unsafe_allow_html=True)
                else:
                    st.info("Not enough data to find matching keywords.")
            
            with tab4:
                st.subheader("Resume Feedback & Suggestions")
                for item in suggestions:
                    if item["impact"] == "High":
                        st.error(f"**{item['type']}**: {item['message']}")
                    elif item["impact"] == "Medium":
                        st.warning(f"**{item['type']}**: {item['message']}")
                    elif item["impact"] == "Low":
                        st.info(f"**{item['type']}**: {item['message']}")
                    else:
                        st.success(f"**{item['type']}**: {item['message']}")
                        
            with tab5:
                st.subheader("Skill Match Analysis")
                # Create a simple dataframe for the chart
                chart_data = pd.DataFrame({
                    "Skill Category": ["Matched", "Missing"],
                    "Count": [len(resume_skills), len(missing_skills)]
                })
                # Using bar chart to visualize skills match vs missing
                st.bar_chart(chart_data.set_index("Skill Category"))
                
            # --- DOWNLOAD REPORT FEATURE ---
            st.markdown("---")
            st.subheader("📥 Download Analysis Report")
            
            # Generate the text report content
            report_text = f"RESUME ANALYSIS REPORT\n"
            report_text += f"{'='*30}\n\n"
            report_text += f"ATS Match Score: {ats_score}%\n"
            report_text += f"Resume Strength: {strength_label} ({strength_score}/100)\n\n"
            
            report_text += "MATCHED SKILLS:\n"
            report_text += ", ".join(resume_skills) if resume_skills else "None found"
            report_text += "\n\n"
            
            report_text += "MISSING SKILLS:\n"
            report_text += ", ".join(missing_skills) if missing_skills else "None missing!"
            report_text += "\n\n"
            
            report_text += "SUGGESTIONS FOR IMPROVEMENT:\n"
            for item in suggestions:
                report_text += f"- [{item['impact']}] {item['type']}: {item['message']}\n"
                
            st.download_button(
                label="Download Full Report (.txt)",
                data=report_text,
                file_name="resume_analysis_report.txt",
                mime="text/plain"
            )
            
            # --- AI RESUME COACH CHATBOT ---
            st.markdown("---")
            st.header("🤖 AI Resume Coach")
            st.markdown("Have questions about your results? 🤖 AI Resume Coach (Beta). Ask me anything!")
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = [
                    {"role": "assistant", "content": "Hi there! I'm your AI Resume Coach. You can ask me things like 'Why is my score low?', 'Which skills should I add?', or 'Can you give me an example of an action verb?'"}
                ]

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("Ask about your score, missing skills, or how to improve..."):
                # Display user message in chat message container
                st.chat_message("user").markdown(prompt)
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Generate AI response
                with st.spinner("Thinking..."):
                    response = generate_chatbot_response(prompt, ats_score, missing_skills, suggestions, text, job_description)
                
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})