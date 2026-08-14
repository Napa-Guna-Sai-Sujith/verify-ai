import re
import logging

logger = logging.getLogger(__name__)

try:
    from langdetect import detect
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

def detect_language(text: str, fallback_pref: str = "English") -> str:
    """
    Detects language using exact Unicode script ranges for Kannada, Telugu, Tamil, Hindi,
    and falls back to langdetect for English / Latin scripts.
    """
    if not text or len(text.strip()) == 0:
        return fallback_pref

    clean_text = text.strip()

    # 1. Check Unicode Script Ranges for Indian Regional Languages
    # Kannada: U+0C80 to U+0CFF
    kan_count = len(re.findall(r'[\u0C80-\u0CFF]', clean_text))
    # Telugu: U+0C00 to U+0C7F
    tel_count = len(re.findall(r'[\u0C00-\u0C7F]', clean_text))
    # Tamil: U+0B80 to U+0BFF
    tam_count = len(re.findall(r'[\u0B80-\u0BFF]', clean_text))
    # Hindi / Devanagari: U+0900 to U+097F
    hin_count = len(re.findall(r'[\u0900-\u097F]', clean_text))

    counts = {
        "Kannada": kan_count,
        "Telugu": tel_count,
        "Tamil": tam_count,
        "Hindi": hin_count
    }

    max_lang, max_cnt = max(counts.items(), key=lambda x: x[1])

    if max_cnt > 2:
        return max_lang

    # 2. Check using langdetect library if non-Indic script
    if LANGDETECT_AVAILABLE:
        try:
            detected_code = detect(clean_text)
            code_map = {
                'kn': 'Kannada',
                'te': 'Telugu',
                'ta': 'Tamil',
                'hi': 'Hindi',
                'en': 'English'
            }
            if detected_code in code_map:
                return code_map[detected_code]
        except Exception as e:
            logger.debug(f"langdetect failed: {e}")

    return fallback_pref or "English"
