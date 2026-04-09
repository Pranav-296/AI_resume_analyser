from pydantic import BaseModel

class AnalyzeResponse(BaseModel):
    score: float
    matched_skills: list
    missing_skills: list
    feedback: str