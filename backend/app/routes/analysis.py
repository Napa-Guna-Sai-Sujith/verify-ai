from fastapi import APIRouter, HTTPException, status
import logging
from typing import Optional, List

from app.models.schemas import AnalyzeRequest, AnalyzeResponse, UrlCheckSchema
from app.services.ocr_service import extract_text_from_image_b64
from app.services.language_service import detect_language
from app.services.verification_service import verify_claims_against_sources
from app.services.ai_service import evaluate_trust_and_explain
from app.services.url_service import extract_urls, analyze_url_safety, strip_urls_from_text
from app.services.localization_service import get_localized_checklist
import re

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Analysis"])

def is_meaningful_message(text: str) -> bool:
    """
    Direct Message Understanding Relevance Check.
    Delegates to claim_service.is_content_relevant, the single source of truth
    for relevance also used downstream by ai_service.evaluate_trust_and_explain.
    (Previously this route kept its own separate, more permissive relevance
    logic here, which could disagree with the downstream check and produce an
    inconsistent "NOT RELEVANT" top-level assessment even when a URL check or
    risk indicator was present in the same response.)
    """
    if not text or not text.strip():
        return False

    from app.services.claim_service import is_content_relevant
    return is_content_relevant(text)

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_content(req: AnalyzeRequest):
    """
    New Verity AI Architecture Endpoint:
    INPUT -> OCR -> URL EXTRACTION & SEPARATION -> DIRECT CONTENT UNDERSTANDING -> EVIDENCE SEARCH -> LINK CHECK -> FINAL ASSESSMENT
    """
    extracted_text = (req.text or "").strip()
    preferred_lang = (req.preferred_language or "English").strip()

    # Step 1: Run OCR ONLY IF text was not already extracted/provided
    if req.image_b64 and not extracted_text:
        extracted_text = extract_text_from_image_b64(req.image_b64, preferred_lang)

    if not extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide raw content text or upload a screenshot to analyze."
        )

    # Step 2: Language Detection (Language of submitted input)
    detected_lang = detect_language(extracted_text, fallback_pref="English")

    # Step 3: Extract & Separate Complete Intact URLs (Never split at '.', '/', ':', '?', '&', '=')
    text_without_urls, extracted_urls = strip_urls_from_text(extracted_text)

    # Step 4: Perform Independent Link Check for all detected URLs
    url_checks: List[UrlCheckSchema] = []
    risk_indicators: List[str] = []

    for u in extracted_urls:
        check = analyze_url_safety(u, extracted_text, "")
        if check:
            url_checks.append(check)
            if check.status in ["SUSPICIOUS", "INVALID"]:
                risk_indicators.append(f"Suspicious or Lookalike Link Detected: {check.url}")

    primary_url_check = url_checks[0] if url_checks else None

    # Step 5: Check Relevance of Message Text
    has_meaningful_message = is_meaningful_message(text_without_urls)

    # Step 6: IF NO MEANINGFUL TEXT MESSAGE (e.g. Standalone URL input or pure CTA/greetings)
    if not has_meaningful_message:
        # Case A: URL Present -> Standalone URL Link Check ONLY (0 Web Searches, No Trust Score!)
        if primary_url_check:
            assessment = primary_url_check.status_label
            explanation = (
                f"No factual message was detected in the submission.\n\n"
                f"• Link: {primary_url_check.url}\n"
                f"• Status: {primary_url_check.status_label}\n"
                f"• Reason: {primary_url_check.reason}"
            )
            recommendation = (
                "Review the Link Check status above. If the link is marked suspicious or unverified, "
                "do not click or enter personal details."
            )
            return AnalyzeResponse(
                detected_language=detected_lang,
                preferred_language=preferred_lang,
                extracted_text=extracted_text,
                claims=[],
                claim_topic="Technology / Security",
                assessment=assessment,
                trust_score=None,  # NO Trust Score generated for standalone URL!
                explanation=explanation,
                recommendation=recommendation,
                risk_indicators=risk_indicators,
                url_check=primary_url_check,
                url_checks=url_checks,
                detected_content_types=["URL"],
                sources=[],        # 0 Web Searches for raw URL!
                before_you_share=get_localized_checklist(preferred_lang)
            )

        # Case B: No URL and No Meaningful Message -> Return ⚠️ NOT RELEVANT
        assessment, trust_score, explanation, recommendation, target_pref_lang, checklist, assigned_topic = evaluate_trust_and_explain(
            text=extracted_text,
            claims=[],
            detected_lang=detected_lang,
            preferred_lang=preferred_lang,
            sources=[]
        )
        return AnalyzeResponse(
            detected_language=detected_lang,
            preferred_language=target_pref_lang,
            extracted_text=extracted_text,
            claims=[],
            claim_topic=assigned_topic,
            assessment=assessment,
            trust_score=None,
            explanation=explanation,
            recommendation=recommendation,
            risk_indicators=[],
            url_check=None,
            url_checks=[],
            detected_content_types=["IRRELEVANT"],
            sources=[],
            before_you_share=checklist
        )

    # Step 7: MEANINGFUL MESSAGE PRESENT -> Direct Content Understanding & Evidence Search
    full_message_claim = text_without_urls.strip()
    
    # Extract Risk Indicators for forwarding/urgency
    raw_text_val = extracted_text
    if any(pat in raw_text_val or re.search(pat, raw_text_val.lower()) for pat in [
        "share immediately", "forward to", "share with", "apply here",
        "షేర్ చేయండి", "పంపండి", "షేర్", "శేರ್ ಮಾಡಿ", "பகிருங்கள்", "शेयर करें"
    ]):
        if "Urgent message forwarding pressure detected." not in risk_indicators:
            risk_indicators.append("Urgent message forwarding pressure detected.")

    # Topic classification for direct message
    from app.services.claim_service import classify_claim_topic
    claim_topic = classify_claim_topic(full_message_claim, [full_message_claim])

    # Direct Evidence Verification on complete message (no claim extraction splitting!)
    sources = verify_claims_against_sources([full_message_claim], full_message_claim, claim_topic)

    assessment, trust_score, explanation, recommendation, target_pref_lang, checklist, assigned_topic = evaluate_trust_and_explain(
        text=full_message_claim,
        claims=[full_message_claim],
        detected_lang=detected_lang,
        preferred_lang=preferred_lang,
        sources=sources,
        url_check=primary_url_check
    )

    # Automatically persist analysis to Neon PostgreSQL DB if user_id is provided
    if req.user_id:
        try:
            from app.services.db_service import save_analysis_record
            save_analysis_record(
                user_id=req.user_id,
                input_type=req.input_type or "text",
                input_text=extracted_text,
                detected_language=detected_lang,
                claims=[full_message_claim],
                assessment=assessment,
                trust_score=trust_score,
                explanation=explanation,
                recommendation=recommendation,
                sources=[s.dict() for s in sources] if sources else []
            )
        except Exception as db_err:
            logger.warning(f"Failed to auto-save analysis to Neon DB: {db_err}")

    return AnalyzeResponse(
        detected_language=detected_lang,
        preferred_language=target_pref_lang,
        extracted_text=extracted_text,
        claims=[],  # Claim Analysis removed! No arbitrary claim fragments!
        claim_topic=assigned_topic or claim_topic,
        assessment=assessment,
        trust_score=trust_score,
        explanation=explanation,
        recommendation=recommendation,
        risk_indicators=risk_indicators,
        url_check=primary_url_check,
        url_checks=url_checks,
        detected_content_types=["MESSAGE_TEXT"] + (["URL"] if url_checks else []),
        sources=sources,
        before_you_share=checklist
    )

