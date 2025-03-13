from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_with_job(resume_text: str, job_description: str):
    """
    Matches the resume text with the job description using TF-IDF + Cosine Similarity.
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    
    score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100
    feedback = ["Your resume matches well with the job description." if score > 70 else "Consider improving your resume to match better."]
    
    return round(score, 2), feedback
