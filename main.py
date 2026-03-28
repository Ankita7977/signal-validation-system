from fastapi import FastAPI, HTTPException
from src.pipeline import run_pipeline

app = FastAPI()


@app.post("/validate")
def validate(event: dict):
    try:
        # 🔥 Send raw event to pipeline
        result = run_pipeline([event])

        # Return first (single input expected)
        return result[0]

    except Exception as e:
        # 🚨 Proper API error handling
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )