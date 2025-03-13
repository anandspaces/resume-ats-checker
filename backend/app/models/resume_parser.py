import re
import spacy
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from transformers import pipeline

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

    def extract_entities(self, text: str) -> dict:
        """Extract structured information from resume text"""
        return {
            "personal_info": self._extract_personal_info(text),
            "skills": self._extract_skills(text),
            "experience": self._extract_experience(text)
        }

    def _extract_personal_info(self, text: str) -> dict:
        return {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text)
        }

    def _extract_name(self, text: str) -> str:
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Not Found"

    def _extract_email(self, text: str) -> str:
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        matches = re.findall(email_regex, text)
        for email in matches:
            try:
                validate_email(email)
                return email
            except EmailNotValidError:
                continue
        return "Not Found"

    def _extract_phone(self, text: str) -> str:
        phone_numbers = []
        for match in phonenumbers.PhoneNumberMatcher(text, "US"):
            phone_numbers.append(phonenumbers.format_number(
                match.number,
                phonenumbers.PhoneNumberFormat.E164
            ))
        return phone_numbers[0] if phone_numbers else "Not Found"

    def _extract_skills(self, text: str) -> list:
        skills = set()
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["SKILL", "TECH"]:
                skills.add(ent.text.lower())
                
        patterns = [
            r"(?i)(?:proficient in|expertise in|skills?:?)\s*((?:\w+\s*)+)",
            r"\b(?:python|java|javascript|react|aws|docker|kubernetes)\b"
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    skills.update(s.strip().lower() for s in match[0].split(','))
                else:
                    skills.add(match.lower())
        
        return sorted(skills)

    def _extract_experience(self, text: str) -> dict:
        doc = self.nlp(text)
        return {
            "organizations": [ent.text for ent in doc.ents if ent.label_ == "ORG"][:3],
            "dates": [ent.text for ent in doc.ents if ent.label_ == "DATE"][:3],
            "titles": re.findall(r"(?i)\b(?:Senior|Junior)?\s*(Software Engineer|Developer|Data Scientist|Analyst)\b", text)[:3]
        }