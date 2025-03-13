import os
import torch
import pdfminer.high_level
from transformers import pipeline
from app.models.job_matcher import match_resume_with_job
from app.utils.file_handler import save_uploaded_file

# Load NLP-based Named Entity Recognition (NER) Model
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")

# Load Pre-trained ANN model (if available)
MODEL_PATH = "app/models/ats_model.pkl"
ann_model = torch.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

async def analyze_resume(resume_file, job_description: str):
    saved_path = await save_uploaded_file(resume_file)

    # Extract text from resume
    text = pdfminer.high_level.extract_text(saved_path)

    # Extract skills using NLP
    skills = extract_skills(text)

    # Match with job description
    score, feedback = match_resume_with_job(text, job_description)

    return {"score": score, "details": feedback, "extracted_skills": skills}

def extract_skills(text):
    entities = ner_pipeline(text)
    skills = [ent["word"] for ent in entities if ent["entity"] == "B-SKILL"]
    return list(set(skills))
