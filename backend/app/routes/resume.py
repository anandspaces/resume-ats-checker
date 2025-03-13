from fastapi import APIRouter, UploadFile, File, Form
from app.services.ats_scoring import analyze_resume

router = APIRouter(prefix="/resume", tags=["Resume Analysis"])

@router.post("/analyze")
async def analyze_resume_endpoint(resume: UploadFile = File(...), job_description: str = Form(...)):
    return await analyze_resume(resume, job_description)
