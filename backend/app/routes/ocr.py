from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import logging
from app.services.ocr_service import extract_ocr_from_image_b64

logger = logging.getLogger(__name__)
router = APIRouter(tags=["OCR"])

class OcrRequest(BaseModel):
    image_b64: str
    preferred_language: Optional[str] = "English"

class OcrResponse(BaseModel):
    extracted_text: str
    status: str
    message: str
    ocr_engine_available: bool
    available_languages: List[str]

@router.post("/ocr", response_model=OcrResponse)
def perform_ocr(req: OcrRequest):
    """
    Dedicated OCR endpoint to extract text from screenshot image
    and return editable text for user review before running main analysis.
    """
    if not req.image_b64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide base64 image data."
        )

    res = extract_ocr_from_image_b64(req.image_b64, req.preferred_language or "English")
    return OcrResponse(
        extracted_text=res["extracted_text"],
        status=res["status"],
        message=res["message"],
        ocr_engine_available=res["ocr_engine_available"],
        available_languages=res["available_languages"]
    )
