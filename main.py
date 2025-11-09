from fastapi import FastAPI
from app.config import app as configured_app

# FastAPI 앱 실행
app = configured_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
