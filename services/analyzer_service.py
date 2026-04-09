from ml.pipeline import analyze_resume

async def process_analysis(resume_file, job_description):
    try:
        content = await resume_file.read()
        text = content.decode("utf-8", errors="ignore")

        result = analyze_resume(text, job_description)

        return result

    except Exception as e:
        return {"error": str(e)}