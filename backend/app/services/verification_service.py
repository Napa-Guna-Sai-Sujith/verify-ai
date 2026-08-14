import logging
import re
from typing import List, Dict, Set, Tuple
from urllib.parse import urlparse
from app.models.schemas import SourceSchema

logger = logging.getLogger(__name__)

# Try importing ddgs (new name) or duckduckgo_search (old name)
DDG_AVAILABLE = False
try:
    from ddgs import DDGS
    DDG_AVAILABLE = True
except ImportError:
    try:
        from duckduckgo_search import DDGS
        DDG_AVAILABLE = True
    except ImportError:
        logger.warning("ddgs/duckduckgo_search package not installed. Evidence search unavailable.")

STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "if", "because", "as", "what", "which",
    "this", "that", "these", "those", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "to", "from", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "can", "will", "just", "should", "now",
    "you", "your", "yours", "for", "with", "message", "forward", "share", "immediately"
}

GENERIC_HOMEPAGES: Set[str] = {
    "youtube.com", "www.youtube.com", "m.youtube.com",
    "facebook.com", "www.facebook.com", "m.facebook.com",
    "twitter.com", "www.twitter.com", "x.com",
    "google.com", "www.google.com", "google.co.in",
    "india.gov.in", "www.india.gov.in",
    "instagram.com", "www.instagram.com"
}

def is_generic_homepage(url: str) -> bool:
    """Returns True if URL is a generic homepage without a specific article path."""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.strip("/")

        if domain in GENERIC_HOMEPAGES and (not path or path in ["feed", "home", "index.html"]):
            return True
        if not path and domain in GENERIC_HOMEPAGES:
            return True
        return False
    except Exception:
        return True

def extract_claim_keywords(claims: List[str], full_text: str) -> Set[str]:
    """Extracts meaningful topic keywords from claims or text, ignoring stop words."""
    combined = (" ".join(claims) + " " + full_text).lower()
    words = re.findall(r"\b[a-zA-Z0-9]{3,}\b", combined)
    return {w for w in words if w not in STOPWORDS}

def generate_dynamic_search_queries(claim_topic: str, claims: List[str], text: str) -> List[str]:
    """
    Generates targeted, claim-specific search queries based on the claim content and topic category.
    Does NOT use hard-coded generic queries.
    """
    primary_claim = claims[0] if claims else text
    keywords = list(extract_claim_keywords(claims, text))
    key_phrase = " ".join(keywords[:5]) if keywords else primary_claim[:50]

    queries = []

    if claim_topic == "Health / Medical":
        queries.append(f"{key_phrase} fact check medical evidence")
        queries.append(f"{key_phrase} cure treatment research")
    elif claim_topic == "Weather / Advisory":
        queries.append(f"{key_phrase} school closure rain weather alert")
        queries.append(f"{key_phrase} official weather announcement")
    elif claim_topic == "Financial Scam / Viral":
        queries.append(f"{key_phrase} reward scam viral message fact check")
        queries.append(f"{key_phrase} money claim hoax")
    elif claim_topic == "Education":
        queries.append(f"{key_phrase} education department announcement")
        queries.append(f"{key_phrase} official scholarship exam notification")
    elif claim_topic == "Science / Astronomy":
        queries.append(f"{key_phrase} astronomy fact check science")
        queries.append(f"{key_phrase} scientific observation evidence")
    elif claim_topic == "Entertainment":
        queries.append(f"{key_phrase} movie release date announcement")
        queries.append(f"{key_phrase} official news")
    elif claim_topic == "Government / Public Policy":
        queries.append(f"{key_phrase} government scheme official announcement")
        queries.append(f"{key_phrase} PIB fact check circular")
    else:
        queries.append(f"{key_phrase} fact check verification")
        queries.append(f"{key_phrase} official news report")

    return list(dict.fromkeys(queries))

def evaluate_evidence_status(title: str, snippet: str, keywords: Set[str], topic: str) -> Tuple[str, int]:
    """
    Classifies a candidate source into:
    - SUPPORTS CLAIM
    - CONTRADICTS CLAIM
    - RELATED BUT INCONCLUSIVE
    Calculates relevance score (0 to 100).
    """
    combined_text = (title + " " + snippet).lower()

    # 1. Relevance Score
    matches = sum(1 for kw in keywords if kw in combined_text)
    if not keywords:
        relevance_score = 50
    else:
        relevance_score = int((matches / len(keywords)) * 100)
        if matches >= 2:
            relevance_score += 20
        if matches >= 4:
            relevance_score += 20

    relevance_score = min(100, max(0, relevance_score))

    # 2. Evidence Status Classification
    debunk_terms = ["fake", "hoax", "false", "busted", "misleading", "scam", "unfounded", "no evidence", "refutes", "denies", "myth", "fake news"]
    support_terms = ["confirmed", "official announcement", "approved", "verified", "issued circular", "launches", "notifies", "valid"]

    if any(dt in combined_text for dt in debunk_terms):
        evidence_status = "CONTRADICTS CLAIM"
    elif any(st in combined_text for st in support_terms) and relevance_score >= 50:
        evidence_status = "SUPPORTS CLAIM"
    else:
        evidence_status = "RELATED BUT INCONCLUSIVE"

    return evidence_status, relevance_score

def get_source_type_for_domain(domain: str, topic: str) -> str:
    """Returns appropriate source type based on URL domain and claim topic."""
    d = domain.lower()
    if ".gov" in d or "pib.gov" in d or "nic.in" in d:
        return "Official Government Source"
    elif any(fc in d for fc in ["factcheck", "altnews", "boomlive", "snopes", "pib", "vishvasnews"]):
        return "Certified Fact-Checker"
    elif topic == "Health / Medical" and any(m in d for m in ["who.int", "cdc.gov", "nih.gov", "icmr", "pubmed", "medline"]):
        return "Official Medical / Health Authority"
    elif topic == "Weather / Advisory" and any(w in d for w in ["imd.gov", "accuweather", "weather.com", "meteo"]):
        return "Official Meteorological Source"
    elif topic == "Science / Astronomy" and any(s in d for s in ["nasa.gov", "isro.gov", "space.com", "nature.com"]):
        return "Official Scientific Source"
    elif any(news in d for news in ["thehindu", "indianexpress", "ndtv", "bbc", "reuters", "timesofindia", "deccanherald"]):
        return "Reputable News Organization"
    else:
        return "Authoritative Regional Source"

def verify_claims_against_sources(claims: List[str], text_query: str, claim_topic: str) -> List[SourceSchema]:
    """
    Executes claim-driven multi-query evidence search.
    Classifies candidate sources into SUPPORTS CLAIM / CONTRADICTS CLAIM / RELATED BUT INCONCLUSIVE.
    Filters out generic domain homepages and unrelated links.
    """
    sources: List[SourceSchema] = []
    
    if not text_query or len(text_query.strip()) < 3:
        return sources

    keywords = extract_claim_keywords(claims, text_query)
    queries = generate_dynamic_search_queries(claim_topic, claims, text_query)

    if not DDG_AVAILABLE:
        logger.warning("DuckDuckGo search not available. Returning empty sources list.")
        return sources

    seen_urls: Set[str] = set()

    for q in queries:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(q, max_results=4))
                for item in results:
                    url = item.get("href", "")
                    title = item.get("title", "")
                    body = item.get("body", "")

                    if not url or url in seen_urls or is_generic_homepage(url):
                        continue

                    evidence_status, relevance_score = evaluate_evidence_status(title, body, keywords, claim_topic)

                    # Reject UNRELATED candidate sources (< 25% overlap)
                    if relevance_score < 25:
                        continue

                    parsed_domain = urlparse(url).netloc
                    source_type = get_source_type_for_domain(parsed_domain, claim_topic)

                    relevance_desc = body[:160] if body else f"Directly addresses {claim_topic.lower()} claim. Relevance overlap: {relevance_score}%."

                    sources.append(
                        SourceSchema(
                            title=title[:100],
                            url=url,
                            source_type=source_type,
                            relevance=relevance_desc,
                            claim_topic=claim_topic,
                            evidence_status=evidence_status
                        )
                    )
                    seen_urls.add(url)

                    if len(sources) >= 3:
                        break
        except Exception as err:
            logger.warning(f"Live search exception for query '{q}': {err}")

        if len(sources) >= 3:
            break

    return sources[:3]
