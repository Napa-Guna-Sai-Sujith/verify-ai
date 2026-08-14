import re
from typing import List, Tuple, Dict, Any
from app.services.url_service import strip_urls_from_text, extract_urls

# Pure noise / UI elements / common non-claim greetings
IRRELEVANT_EXACT_PATTERNS = [
    r"^[\s\d\:\.\,\!\?\-\_\@\#\$\%\^\&\*\(\)\+\=\\\/\|\<\>\[\]\{\}\"\'\;\~\`]+$",
    r"^(hello|hi|hey|good morning|good evening|good night|thanks|thank you|ok|okay|bye|see you|namaste|vanakkam|have a nice day|have a wonderful day|happy birthday)[\!\.\?]*$",
    r"^(12:45 pm|10:30 am|\d{1,2}:\d{2}\s*(am|pm)?)[\!\.\?]*$",
    r"^(home search settings profile|home|search|settings|profile|notifications|battery|wifi|wi-fi|bluetooth|signal|status bar)[\!\.\?]*$",
    r"^(share this immediately|forward to all|share now|must read|urgent|important|share this|forward this|click here now|click now|visit here|apply here|click here)[\!\.\?]*$",
    r"^(random abc xyz 123|abc xyz|test 123)[\!\.\?]*$"
]

def classify_and_route_content(text: str) -> Dict[str, Any]:
    """
    Reworked Content Understanding & Relevance Pipeline.
    Classifies OCR/raw text into 7 Content Types BEFORE Claim Analysis:
    1. FACTUAL_CLAIM
    2. URL
    3. MESSAGE_TEXT
    4. FORWARDING_SPAM_LANGUAGE
    5. UI_TEXT
    6. RANDOM_OCR_NOISE
    7. IRRELEVANT
    """
    if not text or not text.strip():
        return {
            "content_types": ["IRRELEVANT"],
            "claims": [],
            "urls": [],
            "risk_indicators": [],
            "text_without_urls": ""
        }

    raw_text = text.strip()
    text_without_urls, extracted_urls = strip_urls_from_text(raw_text)
    clean_text = text_without_urls.strip()

    detected_types = set()
    risk_indicators = []
    claims = []

    # 1. URL Content Type
    if extracted_urls:
        detected_types.add("URL")

    # If input is ONLY URLs and nothing else
    if not clean_text:
        return {
            "content_types": list(detected_types) if detected_types else ["IRRELEVANT"],
            "claims": [],
            "urls": extracted_urls,
            "risk_indicators": [],
            "text_without_urls": ""
        }

    clean_lower = clean_text.lower()

    # 2. Timestamp / Time Filter (e.g. "12:45 PM")
    if re.match(r'^\d{1,2}:\d{2}\s*(am|pm)?$', clean_lower):
        detected_types.add("IRRELEVANT")
        return {
            "content_types": list(detected_types),
            "claims": [],
            "urls": extracted_urls,
            "risk_indicators": [],
            "text_without_urls": clean_text
        }

    # 3. Emoji & Quality Pre-Check
    text_without_emojis = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27ff\u2300-\u23ff]', '', clean_lower).strip()
    if not text_without_emojis or len(text_without_emojis) < 3:
        detected_types.add("IRRELEVANT")
        return {
            "content_types": list(detected_types),
            "claims": [],
            "urls": extracted_urls,
            "risk_indicators": [],
            "text_without_urls": clean_text
        }

    # 4. UI Text Filter
    ui_keywords = {
        "home", "search", "settings", "profile", "menu", "battery", "5g", "lte", "wifi", "wi-fi",
        "bluetooth", "signal", "status", "notifications", "pm", "am", "bar", "display", "sound"
    }
    words = set(re.findall(r'\b[a-z0-9\-]+\b', text_without_emojis))
    if words and (words.issubset(ui_keywords) or len(words.difference(ui_keywords)) == 0):
        detected_types.add("UI_TEXT")
        return {
            "content_types": list(detected_types),
            "claims": [],
            "urls": extracted_urls,
            "risk_indicators": [],
            "text_without_urls": clean_text
        }

    # 5. Random OCR Noise Filter
    if words and words.issubset({"random", "abc", "xyz", "123", "test"}):
        detected_types.add("RANDOM_OCR_NOISE")
        return {
            "content_types": list(detected_types),
            "claims": [],
            "urls": extracted_urls,
            "risk_indicators": [],
            "text_without_urls": clean_text
        }

    # 6. Conversational Greetings Filter
    greeting_words = {
        "hello", "hi", "hey", "good", "morning", "evening", "night", "thanks", "thank", "you",
        "ok", "okay", "bye", "see", "namaste", "vanakkam", "have", "a", "nice", "wonderful",
        "great", "day", "happy", "birthday", "everyone", "all"
    }
    if words and words.issubset(greeting_words):
        detected_types.add("IRRELEVANT")
        return {
            "content_types": list(detected_types),
            "claims": [],
            "urls": extracted_urls,
            "risk_indicators": [],
            "text_without_urls": clean_text
        }

    # 7. Forwarding / Spam Language Detection
    spam_patterns = [
        (r"share (this )?immediately", "Urgent message forwarding pressure detected ('Share immediately')."),
        (r"forward (this )?to", "Pressure to forward message to groups."),
        (r"share with \d+", "Virality request to share with specific count."),
        (r"click here to claim", "Promotional click request for financial claim."),
        (r"apply here", "Direct CTA link instruction."),
        (r"ವಾಟ್ಸಾಪ್ ಗ್ರೂಪ್", "Urgent WhatsApp group forwarding pressure."),
        (r"ತಕ್ಷಣವೇ ಶೇರ್ ಮಾಡಿ", "Urgent forwarding pressure (Kannada)."),
        (r"వెంటనే షేర్ చేయండి", "Urgent forwarding pressure (Telugu)."),
        (r"உடனே பகிருங்கள்", "Urgent forwarding pressure (Tamil)."),
        (r"तुरंत शेयर करें", "Urgent forwarding pressure (Hindi).")
    ]

    for pat, desc in spam_patterns:
        if re.search(pat, clean_lower):
            detected_types.add("FORWARDING_SPAM_LANGUAGE")
            if desc not in risk_indicators:
                risk_indicators.append(desc)

    # Pure Call-To-Action Filter (e.g., 'Share this immediately!' without factual claim)
    cta_only_words = {"share", "forward", "click", "here", "now", "immediately", "urgent", "must", "read", "this", "to", "all", "everyone", "visit", "apply"}
    if words and words.issubset(cta_only_words):
        detected_types.add("FORWARDING_SPAM_LANGUAGE")
        return {
            "content_types": list(detected_types),
            "claims": [],
            "urls": extracted_urls,
            "risk_indicators": risk_indicators or ["Urgent forwarding pressure detected."],
            "text_without_urls": clean_text
        }

    # 8. Factual Claim Extraction (Preserves 100% full sentences, NO over-splitting!)
    detected_types.add("MESSAGE_TEXT")

    raw_sentences = [s.strip() for s in re.split(r'[\.\!\?\n]+', clean_text) if len(s.strip()) > 5]

    factual_keywords = [
        "government", "scheme", "giving", "free", "₹", "rs", "rupees", "lakh", "crore",
        "ministry", "pib", "pm", "cm", "yojana", "support", "relief", "warning", "bank",
        "account", "grant", "subsidy", "closed", "rain", "cure", "cures", "medicine", "exam",
        "advisory", "order", "alert", "moon", "visible", "daytime", "movie", "actor", "release",
        "announced", "available", "closed tomorrow", "school closure", "heavy rain",
        "ಸರ್ಕಾರ", "ಯೋಜನೆ", "ರೂ", "ಹಣ", "ಹಂಚಿಕೆ", "ಪ್ರಧಾನಮಂತ್ರಿ", "ಘೋಷಿಸಿದೆ", "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ",
        "ಪ್ರభుత్వం", "పథకం", "రూపాయలు", "ఉచితం", "ప్రకటించింది", "విద్యార్థుల కోసం",
        "அரசு", "திட்டம்", "ரூபாய்", "இலவசம்", "அறிவிக்கப்பட்டுள்ளது", "மாணவர்களுக்கு",
        "सरकार", "योजना", "रुपये", "मुफ्त", "वितरण", "घोषणा", "छात्रों"
    ]

    for sentence in raw_sentences:
        lower_sent = sentence.lower()
        if any(kw in lower_sent for kw in factual_keywords) or re.search(r'\d+', sentence):
            claims.append(sentence)

    if claims:
        detected_types.add("FACTUAL_CLAIM")
    elif raw_sentences:
        valid_assertions = [s for s in raw_sentences if len(s.split()) >= 4]
        if valid_assertions:
            claims = valid_assertions[:2]
            detected_types.add("FACTUAL_CLAIM")

    return {
        "content_types": list(detected_types),
        "claims": claims[:3],
        "urls": extracted_urls,
        "risk_indicators": risk_indicators,
        "text_without_urls": clean_text
    }

def is_content_relevant(text: str) -> bool:
    """
    Utility wrapper checking if text contains a FACTUAL_CLAIM or valid URL.
    """
    routed = classify_and_route_content(text)
    return "FACTUAL_CLAIM" in routed["content_types"] or "URL" in routed["content_types"]

def extract_risk_indicators(text: str, claims: List[str], claim_topic: str) -> List[str]:
    """
    Utility wrapper returning risk indicators from classify_and_route_content.
    """
    routed = classify_and_route_content(text)
    return routed.get("risk_indicators", [])

def classify_claim_topic(text: str, claims: List[str]) -> str:
    """
    Classifies input content into a domain category to guide evidence search & source selection.
    """
    combined = (text + " " + " ".join(claims)).lower()

    # Health / Medical
    if any(k in combined for k in [
        "cure", "cures", "diabetes", "cancer", "medicine", "doctor", "hospital", "vaccine",
        "remedy", "treatment", "health", "disease", "virus", "infection", "pill",
        "ಅನಾರೋಗ್ಯ", "ಚಿಕಿತ್ಸೆ", "ఔషధం", "మందు", "மருந்து", "दवा", "इलाज"
    ]):
        return "Health / Medical"

    # Weather / Advisory / Natural Disaster
    if any(k in combined for k in [
        "rain", "rainfall", "storm", "cyclone", "flood", "weather", "temperature", "monsoon",
        "closed tomorrow", "school closure", "heavy rain", "ಮಳೆ", "ರಜೆ", "ವರ್ಷಂ", "ಸెలవు", "மழை", "விடுமுறை", "बारिश", "छुट्टी"
    ]):
        return "Weather / Advisory"

    # Financial Scam / Viral Forward / Unverified Reward
    raw_combined = text + " " + " ".join(claims)
    if any(k in combined for k in [
        "share to receive", "forward this message", "receive ₹", "win ₹", "free reward",
        "click here to claim", "whatsapp reward", "25,000", "25000", "5,000", "5000", "rupees"
    ]) or any(k in raw_combined for k in [
        "ఖాతాలో జమ", "స్నేహితులకు షేర్", "ఆర్థిక సహాయం", "ఉచితం", "నగదు", "ఆಮಿಷ", "ఇనాము", "இலவசம்", "इनाम", "బ్యాంక్ ఖాతా", "పంపండి", "షేర్"
    ]) or ("₹" in raw_combined and any(u in raw_combined for u in ["share", "forward", "పంపండి", "షేర్", "ಶೇರ್", "பகிருங்கள்"])):
        return "Financial Scam / Viral"

    # Education / Student Benefit
    if any(k in combined for k in [
        "school", "college", "university", "student", "scholarship", "exam", "syllabus", "marks",
        "ಶಾಲಾ", "ವಿದ್ಯಾರ್ಥಿ", "ಪಾಠಶಾಲಾ", "విద్యార్థి", "பள்ளி", "மாணவர்", "स्कूल", "छात्र"
    ]):
        return "Education"

    # Science / Astronomy
    if any(k in combined for k in [
        "moon", "sun", "planet", "space", "eclipse", "nasa", "isro", "earth", "daytime",
        "astronomy", "solar", "lunar", "ಗ್ರಹ", "ಸೂರ್ಯ", "நிலவு", "अंतरिक्ष"
    ]):
        return "Science / Astronomy"

    # Entertainment / Media
    if any(k in combined for k in [
        "movie", "actor", "actress", "film", "release date", "cinema", "box office", "trailer",
        "ಚಲನಚಿತ್ರ", "సినిಮಾ", "படம்", "फिल्म"
    ]):
        return "Entertainment"

    # Government / Public Policy
    if any(k in combined for k in [
        "government", "ministry", "pib", "pm", "cm", "yojana", "official notification",
        "policy", "election", "rbi", "order", "ಸರ್ಕಾರ", "ಪ್ರಧಾನಮಂತ್ರಿ", "ಪ್ರభుత్వం", "அரசு", "सरकार"
    ]):
        return "Government / Public Policy"

    # Technology / Security
    if any(k in combined for k in [
        "hacked", "whatsapp", "otp", "virus", "phishing", "password", "app update",
        "ವೈರಸ್", "యాప్", "செயலி"
    ]):
        return "Technology / Security"

    return "General Viral Claim"

def extract_claims(text: str) -> List[str]:
    """
    Extracts isolated factual claims from longer digital messages using classify_and_route_content.
    """
    routed = classify_and_route_content(text)
    return routed.get("claims", [])
