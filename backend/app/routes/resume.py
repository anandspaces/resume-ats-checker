from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.ats_scoring import ATSAnalyzer, generate_detailed_feedback
from app.models.resume_parser import ResumeParser
from app.utils.file_handler import save_temp_file
from app.utils.text_processing import extract_text_from_pdf, extract_text_from_docx, extract_resume_sections

router = APIRouter(prefix="/resume", tags=["Resume Analysis"])

@router.post("/analyze")
async def analyze_resume_endpoint(
    resume: UploadFile = File(..., description="Resume file (PDF/DOCX)"),
    job_description: str = Form(..., description="Job description text")
):
    try:
        file_path = await save_temp_file(resume)
        
        # Text extraction
        if resume.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif resume.filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        
        # Analysis
        analyzer = ATSAnalyzer()
        parser = ResumeParser()
        
        sections = extract_resume_sections(text)
        score = analyzer.calculate_score(text, job_description)
        entities = parser.extract_entities(text)
        feedback = generate_detailed_feedback(sections, job_description)
        
        return {
            "score": round(score, 1),
            "feedback": feedback,
            "entities": entities,
            "sections": sections
        }
        
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=str(e))