import PyPDF2
import docx
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


# Extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text


# Detect file type
def extract_resume_text(file):
    if file.name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif file.name.endswith('.docx'):
        return extract_text_from_docx(file)
    else:
        return ""


# Skill database
SKILLS_DB = [
    "python", "java", "c++", "html", "css", "javascript",
    "react", "node", "machine learning", "deep learning",
    "data analysis", "sql", "mongodb", "git", "docker",
    "tensorflow", "pandas", "numpy"
]


# Extract skills
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


# Calculate similarity (ATS score)
def calculate_similarity(resume_text, job_description):
    texts = [resume_text, job_description]

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(texts)

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return round(score[0][0] * 100, 2)

def get_missing_skills(resume_skills, job_description):
    jd_skills = extract_skills(job_description)
    
    missing = []
    for skill in jd_skills:
        if skill not in resume_skills:
            missing.append(skill)
    
    return missing