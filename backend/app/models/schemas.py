from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AnalyzeRequest(BaseModel):
    text: Optional[str] = Field(default="", description="Raw message text to analyze")
    image_b64: Optional[str] = Field(default=None, description="Base64 encoded image string for OCR")
    preferred_language: Optional[str] = Field(default="English", description="User preferred language for analysis result & explanation")
    user_id: Optional[str] = Field(default=None, description="User ID to persist analysis into Neon PostgreSQL database")
    input_type: Optional[str] = Field(default="text", description="Input type (text or screenshot)")


class SourceSchema(BaseModel):
    title: str
    url: str
    source_type: str = "Official Source"
    relevance: str
    claim_topic: Optional[str] = "General"
    evidence_status: Optional[str] = "RELATED BUT INCONCLUSIVE"

class UrlCheckSchema(BaseModel):
    url: str
    status: str  # "TRUSTED", "SUSPICIOUS", "UNVERIFIED", "INVALID"
    status_label: str
    reason: str

class AnalyzeResponse(BaseModel):
    detected_language: str
    preferred_language: str = "English"
    extracted_text: str
    claims: List[str] = []
    claim_topic: Optional[str] = "General"
    assessment: str
    trust_score: Optional[int] = None
    explanation: str
    recommendation: str
    risk_indicators: List[str] = []
    url_check: Optional[UrlCheckSchema] = None
    url_checks: List[UrlCheckSchema] = []
    detected_content_types: List[str] = []
    sources: List[SourceSchema] = []
    before_you_share: Optional[List[Dict[str, Any]]] = None

class ProfileCreateRequest(BaseModel):
    full_name: str
    email: str
    preferred_language: Optional[str] = "English"

class ProfileResponse(BaseModel):
    id: str
    full_name: Optional[str] = ""
    email: str
    preferred_language: Optional[str] = "English"
    created_at: Optional[str] = None

