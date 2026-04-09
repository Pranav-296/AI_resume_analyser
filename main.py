from fastapi import FastAPI
from routes.analyze import router as analyze_router

app = FastAPI(title="AI Resume Analyzer Backend")

app.include_router(analyze_router)

@app.get("/")
def root():
    return {"message": "Backend is running"}