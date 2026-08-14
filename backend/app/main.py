from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from app.config import settings
from app.routes import health, analysis, ocr, auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Verity AI Multilingual Digital Trust Platform API",
)

# CORS configuration for local and production Vercel frontend deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Vercel frontend domain and local development
    allow_credentials=True,
    allow_methods=["*"],
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
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
