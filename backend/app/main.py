from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.routes import health, analysis, ocr, auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Verity AI Multilingual Digital Trust Platform API",
)

# Mandatory Security Guideline: Restrict CORS origins to frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(analysis.router, prefix=settings.API_PREFIX)
app.include_router(ocr.router, prefix=settings.API_PREFIX)
app.include_router(auth.router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {
        "project": "Verity AI",
        "tagline": "Check before you trust.",
        "status": "active",
        "health_check": f"{settings.API_PREFIX}/health"
    }

if __name__ == "__main__":
    # Mandatory Security Rule: Listen strictly on localhost / 127.0.0.1
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
