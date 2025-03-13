from fastapi import FastAPI
from app.routes import resume

app = FastAPI(title="Resume ATS Score API", version="1.0")

app.include_router(resume.router)

@app.get("/")
def home():
    return {"message": "Welcome to Resume ATS Score Checker API"}
