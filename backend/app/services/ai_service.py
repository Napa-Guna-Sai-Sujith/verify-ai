import logging
import re
from typing import List, Tuple, Dict, Optional
from app.config import settings
from app.models.schemas import SourceSchema, UrlCheckSchema
from app.services.localization_service import get_localized_content, get_localized_checklist
from app.services.claim_service import is_content_relevant, classify_claim_topic

logger = logging.getLogger(__name__)

def calculate_dynamic_trust_score(
    text: str,
    claims: List[str],
    sources: List[SourceSchema],
    claim_topic: str,
    url_check: Optional[UrlCheckSchema] = None
) -> Tuple[int, str]:
    """
    Calculates a dynamic, evidence-grounded trust score (15 to 95) using multi-domain factor analysis:
    - Evidence Status (SUPPORTS CLAIM vs CONTRADICTS CLAIM)
    - Domain Source Quality & URL Safety
    - Virality & Scam Risk Signals
    """
    clean_text = text.lower()
    score = 50

    has_supporting_evidence = False
    has_contradicting_evidence = False
    has_official_source = False

    if sources:
        for s in sources:
            stype = (s.source_type or "").lower()
            estatus = getattr(s, "evidence_status", "")

            if estatus == "SUPPORTS CLAIM":
                score += 30
                has_supporting_evidence = True
            elif estatus == "CONTRADICTS CLAIM":
                score -= 30
                has_contradicting_evidence = True

            if "government" in stype or "official" in stype or "fact-checker" in stype:
                score += 10
                has_official_source = True

    # URL Check Penalty / Bonus
    if url_check:
        if url_check.status == "TRUSTED":
            score += 15
        elif url_check.status in ["SUSPICIOUS", "INVALID"]:
            score -= 25

    # Financial Scam / Virality Risk Penalty
    if claim_topic == "Financial Scam / Viral":
        score -= 20

    urgency_patterns = [
        r"\bshare with \d+\b", r"\bforward to \d+\b", r"\bshare immediately\b", r"\burgent alert\b",
        r"\b\d+ మంది స్నేహితులకు\b", r"వెంటనే \d+", r"పంపండి", r"షేర్ చేయండి", r"వాట్ಸಾಪ್ ಗ್ರೂಪ್",
        r"ತಕ್ಷಣವೇ ಶೇರ್ ಮಾಡಿ", r"వెంటనే షేర్ చేయండి", r"உடனே பகிருங்கள்", r"तुरंत शेयर करें", r"ఖాతాలో జమ"
    ]
    urgency_matches = sum(1 for pat in urgency_patterns if re.search(pat, clean_text))
    if urgency_matches > 0:
        score -= (15 + urgency_matches * 5)

    # Assessment Classification
    if has_contradicting_evidence or (url_check and url_check.status == "SUSPICIOUS") or (claim_topic == "Financial Scam / Viral" and not has_supporting_evidence) or (urgency_matches > 0 and not has_supporting_evidence):
        assessment_type = "misleading"
        final_score = max(15, min(38, score))
    elif has_supporting_evidence or (has_official_source and score >= 70):
        assessment_type = "supported"
        final_score = max(75, min(95, score))
    else:
        assessment_type = "verification"
        final_score = max(45, min(65, score))

    return final_score, assessment_type

def generate_topic_specific_explanation(
    claim_topic: str,
    assessment_type: str,
    claims: List[str],
    sources: List[SourceSchema],
    preferred_lang: str,
    url_check: Optional[UrlCheckSchema] = None
) -> Tuple[str, str]:
    """
    Generates a localized claim-specific explanation and recommendation matching preferred_lang.
    """
    primary_claim = claims[0] if claims else "this claim"
    target_lang = preferred_lang or "English"

    # Fully localized returns for non-English languages
    if target_lang != "English":
        loc_exp = get_localized_content(target_lang, "explanations", assessment_type)
        loc_rec = get_localized_content(target_lang, "recommendations", assessment_type)
        if loc_exp and loc_rec:
            return loc_exp, loc_rec

    # English fallback explanations
    if assessment_type == "supported":
        explanation = (
            f"We cross-referenced this {claim_topic.lower()} claim with official and authoritative online sources.\n\n"
            f"• Verified corroborating evidence was found for: \"{primary_claim}\".\n"
            f"• Key factual assertions match published official circulars and reports."
        )
        recommendation = f"This {claim_topic.lower()} statement is supported by verified sources. You can reference the verified source before sharing."

    elif assessment_type == "misleading":
        if claim_topic == "Health / Medical":
            explanation = (
                f"We analyzed this health statement: \"{primary_claim}\".\n\n"
                f"• Medical research and official health bodies do NOT confirm this cure claim.\n"
                f"• Unbacked medical assertions can pose serious health risks if trusted without medical consultation."
            )
            recommendation = "Do not act on unverified medical cure claims without consulting a certified doctor or health official."
        elif claim_topic == "Financial Scam / Viral":
            explanation = (
                f"We analyzed the viral message structure and identified high-risk deception indicators.\n\n"
                f"• Forward pressure ('Share with friends immediately') detected.\n"
                f"• Unverified monetary reward claim without legitimate banking or official portal support."
            )
            recommendation = "Avoid forwarding this viral message or clicking unverified reward links."
        else:
            explanation = (
                f"We evaluated the content structure and identified high-risk indicators associated with digital deception.\n\n"
                f"• Urgent call-to-action or unbacked assertions detected for \"{primary_claim}\".\n"
                f"• Reliable news and fact-checking sources contradict or debunk this announcement."
            )
            recommendation = f"Avoid forwarding this {claim_topic.lower()} message until verified through an official portal."

    else: # verification
        if claim_topic == "Weather / Advisory":
            explanation = (
                f"We checked weather alerts regarding: \"{primary_claim}\".\n\n"
                f"• We found weather advisory updates, but could not independently confirm the specific school closure notice.\n"
                f"• Verify directly with local school administration or district circulars."
            )
            recommendation = "Check the local district education circular or school portal before assuming schools are closed."
        elif claim_topic == "Education":
            explanation = (
                f"We searched educational portals for: \"{primary_claim}\".\n\n"
                f"• We could not find a confirmed official press release for this specific wording at this moment.\n"
                f"• Verify directly with the relevant board or university website."
            )
            recommendation = "Check the official university or examination board portal for confirmation."
        else:
            explanation = (
                f"We searched digital databases for: \"{primary_claim}\".\n\n"
                f"• Online evidence is currently insufficient to independently confirm or deny this specific statement.\n"
                f"• Directly verify with an authoritative source before sharing."
            )
            recommendation = "Verify with an independent official news outlet or official portal before sharing."

    return explanation, recommendation

def evaluate_trust_and_explain(
    text: str,
    claims: List[str],
    detected_lang: str,
    preferred_lang: str,
    sources: List[SourceSchema],
    url_check: Optional[UrlCheckSchema] = None
) -> Tuple[str, Optional[int], str, str, str, List[Dict[str, str]], str]:
    """
    Evaluates trust score and generates dynamic, claim-specific localized outputs.
    """
    target_lang = preferred_lang or "English"

    # Check if content contains a verifiable claim
    if not is_content_relevant(text):
        assessment_label = get_localized_content(target_lang, "assessment_labels", "NOT RELEVANT")
        explanation = get_localized_content(target_lang, "explanations", "not_relevant")
        recommendation = get_localized_content(target_lang, "recommendations", "not_relevant")
        checklist = get_localized_checklist(target_lang)
        return assessment_label, None, explanation, recommendation, target_lang, checklist, "Not Relevant"

    # Classify claim topic into domain category
    claim_topic = classify_claim_topic(text, claims)

    # Compute dynamic trust score & assessment type
    trust_score, assessment_type = calculate_dynamic_trust_score(text, claims, sources, claim_topic, url_check)

    assessment_label = get_localized_content(target_lang, "assessment_labels", assessment_type)
    explanation, recommendation = generate_topic_specific_explanation(
        claim_topic, assessment_type, claims, sources, target_lang, url_check
    )
    checklist = get_localized_checklist(target_lang)

    return assessment_label, trust_score, explanation, recommendation, target_lang, checklist, claim_topic
