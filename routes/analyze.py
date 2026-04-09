from fastapi import APIRouter, UploadFile, File, Form
from services.analyzer_service import process_analysis

router = APIRouter()

@router.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    result = await process_analysis(resume, job_description)
    return result