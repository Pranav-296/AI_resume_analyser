import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -----------------------------
# SAFE NLTK SETUP
# -----------------------------
def download_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except:
        nltk.download('punkt')

    try:
        nltk.data.find('corpora/stopwords')
    except:
        nltk.download('stopwords')

download_nltk()

# -----------------------------
# LOAD BERT MODEL
# -----------------------------
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# -----------------------------
# TRAIN SIMPLE ML MODEL
# -----------------------------
train_resumes = [
    "Python developer with machine learning experience",
    "Data scientist with NLP and deep learning",
    "Frontend developer with HTML CSS JavaScript",
    "Marketing and sales expert"
]

train_labels = [1, 1, 0, 0]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(train_resumes)

ml_model = LogisticRegression()
ml_model.fit(X, train_labels)

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
# SKILL SCORE
# -----------------------------
def calculate_skill_score(matched_skills, job_skills):
    if len(job_skills) == 0:
        return 0

    return round((len(matched_skills) / len(job_skills)) * 100, 2)

# -----------------------------
# BERT SIMILARITY
# -----------------------------
def compute_similarity(resume_text, job_description):
    emb1 = bert_model.encode(resume_text, convert_to_tensor=True)
    emb2 = bert_model.encode(job_description, convert_to_tensor=True)

    score = util.pytorch_cos_sim(emb1, emb2)
    return float(score)

# -----------------------------
# ML PREDICTION
# -----------------------------
def predict_resume_score(resume_text):
    vector = vectorizer.transform([resume_text])
    prediction = ml_model.predict(vector)[0]
    return int(prediction)

# -----------------------------
# FINAL SCORE
# -----------------------------
def calculate_final_score(skill_score, similarity_score, ml_prediction):

    similarity_score = similarity_score * 100
    ml_score = ml_prediction * 100

    final_score = (
        0.4 * skill_score +
        0.3 * similarity_score +
        0.3 * ml_score
    )

    return round(final_score, 2)

# -----------------------------
# FEEDBACK
# -----------------------------
def generate_feedback(missing_skills):
    if not missing_skills:
        return "Excellent match for the job."

    return "You should improve the following skills: " + ", ".join(missing_skills)

# -----------------------------
# FINAL PIPELINE
# -----------------------------
def analyze_resume(resume_text, job_description):

    # Preprocess
    resume_tokens = preprocess_text(resume_text)
    job_tokens = preprocess_text(job_description)

    # Skills
    resume_skills = extract_skills(resume_tokens)
    job_skills = extract_skills(job_tokens)

    # Compare
    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    # Scores
    skill_score = calculate_skill_score(matched_skills, job_skills)
    similarity_score = compute_similarity(resume_text, job_description)
    ml_prediction = predict_resume_score(resume_text)

    final_score = calculate_final_score(
        skill_score,
        similarity_score,
        ml_prediction
    )

    # Final output (STRICT FORMAT)
    return {
        "score": final_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "feedback": generate_feedback(missing_skills)
    }