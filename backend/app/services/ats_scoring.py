from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import re

class ATSAnalyzer:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

    def calculate_score(self, resume: str, jd: str) -> float:
        """Combined scoring with TF-IDF and semantic similarity"""
        tfidf_score = self._calculate_tfidf_similarity(resume, jd)
        semantic_score = self._calculate_semantic_similarity(resume, jd)
        return self._combine_scores(tfidf_score, semantic_score)

    def _calculate_tfidf_similarity(self, resume: str, jd: str) -> float:
        vectors = self.tfidf_vectorizer.fit_transform([resume, jd])
        return cosine_similarity(vectors[0], vectors[1])[0][0]

    def _calculate_semantic_similarity(self, resume: str, jd: str) -> float:
        embeddings = self.semantic_model.encode([resume, jd])
        return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    def _combine_scores(self, tfidf: float, semantic: float) -> float:
        return round((tfidf * 0.4 + semantic * 0.6) * 100, 2)

def generate_detailed_feedback(resume_sections: dict, jd: str) -> dict:
    """Generate structured feedback with improvement suggestions"""
    # Combine all sections for keyword analysis
    full_resume_text = ' '.join(resume_sections.values())
    
    feedback = {
        'missing_keywords': [],
        'section_analysis': {},
        'recommendations': []
    }
    
    # Keyword analysis
    jd_keywords = set(re.findall(r'\b\w{3,}\b', jd.lower()))
    resume_keywords = set(re.findall(r'\b\w{3,}\b', full_resume_text.lower()))
    missing = jd_keywords - resume_keywords
    if missing:
        feedback['missing_keywords'] = sorted(missing)[:10]
    
    # Section analysis
    for section, content in resume_sections.items():
        content_keywords = set(re.findall(r'\b\w{3,}\b', content.lower()))
        feedback['section_analysis'][section] = {
            'keyword_match': len(content_keywords & jd_keywords) / len(jd_keywords) if jd_keywords else 0,
            'length_score': min(len(content.split()) / 200, 1)  # Ideal 200 words
        }
    
    # Generate recommendations
    feedback['recommendations'] = [
        *_recommend_based_on_keywords(feedback['missing_keywords']),
        *_recommend_based_on_sections(feedback['section_analysis'])
    ]
    
    return feedback

def _recommend_based_on_keywords(missing_keywords: list) -> list:
    """Generate keyword-based recommendations"""
    recommendations = []
    if missing_keywords:
        rec = f"Add missing keywords: {', '.join(missing_keywords[:5])}"
        recommendations.append(rec)
    return recommendations

def _recommend_based_on_sections(sections: dict) -> list:
    """Generate section-based recommendations"""
    recommendations = []
    for section, analysis in sections.items():
        if analysis['keyword_match'] < 0.3:
            recommendations.append(f"Improve keyword density in {section} section")
        if analysis['length_score'] < 0.5:
            recommendations.append(f"Expand {section} section (currently too short)")
    return recommendations