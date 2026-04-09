import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure required resources (safe for demo use)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# -----------------------------
# SKILL DATABASE
# -----------------------------
SKILLS_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "data analysis", "data science", "nlp", "tensorflow", "pytorch",
    "sql", "mongodb", "docker", "kubernetes", "aws",
    "html", "css", "javascript", "react", "fastapi"
]

# -----------------------------
# PREPROCESSING
# -----------------------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens

# -----------------------------
# SKILL EXTRACTION
# -----------------------------
def extract_skills(tokens):
    extracted_skills = []
    text = " ".join(tokens)

    for skill in SKILLS_DB:
        if skill in text:
            extracted_skills.append(skill)

    return list(set(extracted_skills))

# -----------------------------
# SKILL SCORING
# -----------------------------
def calculate_skill_score(matched_skills, job_skills):
    if len(job_skills) == 0:
        return 0

    score = (len(matched_skills) / len(job_skills)) * 100
    return round(score, 2)

# -----------------------------
# FEEDBACK GENERATION
# -----------------------------
def generate_feedback(missing_skills):
    if not missing_skills:
        return "Excellent match for the job."

    feedback = "You should improve the following skills: "
    feedback += ", ".join(missing_skills)

    return feedback

# -----------------------------
# FINAL PIPELINE FUNCTION
# -----------------------------
def analyze_resume(resume_text, job_description):

    # Preprocess
    resume_tokens = preprocess_text(resume_text)
    job_tokens = preprocess_text(job_description)

    # Extract skills
    resume_skills = extract_skills(resume_tokens)
    job_skills = extract_skills(job_tokens)

    # Compare
    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    # Score
    score = calculate_skill_score(matched_skills, job_skills)

    # Feedback
    feedback = generate_feedback(missing_skills)

    # Final output (DO NOT CHANGE FORMAT)
    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "feedback": feedback
    }
