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
    # Programming Languages
    "python", "java", "c++", "c#", "ruby", "go", "swift", "kotlin", "php", "typescript", "javascript", "r", "matlab",
    # Web Technologies
    "html", "css", "react", "node", "angular", "vue", "django", "flask", "spring", "express", "fastapi",
    # Data Science & ML
    "machine learning", "deep learning", "data analysis", "artificial intelligence", "nlp", "computer vision",
    "tensorflow", "pandas", "numpy", "scikit-learn", "pytorch", "keras", "matplotlib", "seaborn",
    # Databases
    "sql", "mongodb", "postgresql", "mysql", "redis", "cassandra", "elasticsearch", "oracle",
    # DevOps & Cloud
    "git", "docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "ci/cd", "terraform", "ansible", "linux",
    # Others
    "agile", "scrum", "jira", "rest api", "graphql", "microservices", "system design"
]


# Extract skills
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        # Use regex to find exact word boundaries and avoid partial matches
        # We escape the skill to handle special characters, but use the requested regex format
        # If the skill contains non-word characters like ++ or # at the end, \b might fail,
        # but following user instructions exactly:
        if re.search(rf"\b{re.escape(skill)}\b", text) or (skill in ['c++', 'c#'] and skill in text):
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
    # It is expected that job_description is already cleaned before being passed here
    jd_skills = extract_skills(job_description)
    
    missing = []
    for skill in jd_skills:
        if skill not in resume_skills:
            missing.append(skill)
    
    return missing

def get_matched_keywords(resume_text, job_description):
    """Find common words between resume and job description (excluding common stop words)."""
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    
    # Extract words that are 4 characters or longer
    resume_words = set(re.findall(r'\b[a-z]{4,}\b', resume_text))
    jd_words = set(re.findall(r'\b[a-z]{4,}\b', job_description))
    
    # Remove common English stop words
    resume_words = resume_words - ENGLISH_STOP_WORDS
    jd_words = jd_words - ENGLISH_STOP_WORDS
    
    # Find common keywords
    matched_keywords = list(resume_words.intersection(jd_words))
    
    # Return top 20 keywords alphabetically
    return sorted(matched_keywords)[:20]