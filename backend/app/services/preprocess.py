import re
import pdfplumber
import docx
from unidecode import unidecode
from typing import Union
from app.utils.file_handler import save_temp_file

def clean_text(text: str) -> str:
    """
    Cleans and normalizes text by removing special characters, multiple spaces, and non-ASCII characters.
    """
    text = unidecode(text)  # Normalize Unicode characters
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^\w\s.,]", "", text)  # Remove special characters except punctuation
    return text.strip()

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + " "
    return clean_text(text)

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from a DOCX file.
    """
    doc = docx.Document(file_path)
    text = " ".join([para.text for para in doc.paragraphs])
    return clean_text(text)

def preprocess_resume(file: Union[str, bytes], file_type: str) -> str:
    """
    Extracts and preprocesses text from a resume file.
    """
    temp_path = save_temp_file(file, file_type)

    if file_type == "pdf":
        return extract_text_from_pdf(temp_path)
    elif file_type == "docx":
        return extract_text_from_docx(temp_path)
    else:
        raise ValueError("Unsupported file type")
