import re
import pdfplumber
from pdfminer.high_level import extract_text as pdfminer_extract
import docx
from unidecode import unidecode

def clean_text(text: str) -> str:
    text = unidecode(text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,\-/()%]', '', text)
    return text.strip()

def extract_text_from_pdf(file_path: str) -> str:
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text(x_tolerance=1) for page in pdf.pages])
        if len(text.strip()) < 100:
            text = pdfminer_extract(file_path)
        return clean_text(text)
    except Exception as e:
        raise ValueError(f"PDF processing error: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        return clean_text("\n".join([para.text for para in doc.paragraphs]))
    except Exception as e:
        raise ValueError(f"DOCX processing error: {str(e)}")

def extract_resume_sections(text: str) -> dict:
    section_patterns = {
        'experience': r'(experience|work\s+history)',
        'education': r'(education|academic)',
        'skills': r'(skills|technical\s+skills)'
    }
    sections = {k: '' for k in section_patterns}
    current_section = 'header'
    
    for line in text.split('\n'):
        line_lower = line.strip().lower()
        for section, pattern in section_patterns.items():
            if re.search(pattern, line_lower):
                current_section = section
                break
        sections[current_section] += ' ' + line
    
    return {k: clean_text(v) for k, v in sections.items()}