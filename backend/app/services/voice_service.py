from typing import Dict

LANGUAGE_VOICE_MAP: Dict[str, str] = {
    "English": "en-IN",
    "Kannada": "kn-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "Hindi": "hi-IN"
}

def get_voice_lang_tag(language_name: str) -> str:
    """Returns the BCP 47 language tag for browser speech synthesis."""
    return LANGUAGE_VOICE_MAP.get(language_name, "en-IN")
