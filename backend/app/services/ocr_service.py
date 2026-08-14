import base64
import io
import os
import re
import logging
import subprocess
from typing import Dict, Any, List
from PIL import Image, ImageEnhance, ImageStat
from app.config import settings

logger = logging.getLogger(__name__)

LANG_MAP = {
    "English": "eng",
    "Kannada": "kan",
    "Telugu": "tel",
    "Tamil": "tam",
    "Hindi": "hin"
}

def resolve_tesseract_binary() -> str:
    """
    Dynamically locates and sets the Tesseract executable path.
    Checks environment variable TESSERACT_CMD, custom user install paths, and standard OS locations.
    """
    try:
        import pytesseract
    except ImportError:
        return None

    search_paths = [
        os.getenv("TESSERACT_CMD"),
        settings.TESSERACT_CMD,
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
        os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe"),
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract"
    ]

    for p in search_paths:
        if p and os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            return p

    return None

def is_blank_image(image: Image.Image) -> bool:
    """
    Fast Visual Pre-Check (< 5ms):
    Calculates pixel variance across image. If variance < 5.0, image is blank or single solid color.
    """
    try:
        gray = image.convert("L")
        stat = ImageStat.Stat(gray)
        variance = stat.var[0] if stat.var else 0
        return variance < 5.0
    except Exception:
        return False

def optimize_image_for_fast_ocr(image: Image.Image) -> Image.Image:
    """
    Fast Image Optimization:
    - Downscales oversized screenshots (max 1200px) preserving aspect ratio.
    - Lightweight contrast normalization.
    """
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    w, h = image.size
    max_dim = 1200

    if w > max_dim or h > max_dim:
        scale = max_dim / float(max(w, h))
        image = image.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    elif w < 600 or h < 600:
        scale = max(2.0, 800.0 / float(max(w, h)))
        image = image.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)

    gray = image.convert("L")
    enhanced = ImageEnhance.Contrast(gray).enhance(1.4)
    return enhanced

def is_ocr_text_garbage(text: str) -> bool:
    """
    OCR Quality Check:
    Evaluates whether extracted text is unreadable garbage or random OCR noise.
    """
    if not text:
        return True
    clean = text.strip()
    if len(clean) < 3:
        return True

    letters = re.findall(r'[\w\u0900-\u0D7F]', clean)
    symbols = re.findall(r'[^\w\s\u0900-\u0D7F]', clean)

    if len(letters) < 3:
        return True

    total = len(letters) + len(symbols)
    if total > 0 and (len(symbols) / total) > 0.55:
        return True

    return False

def process_ocr_with_diagnostics(image_b64: str, preferred_lang: str = "English") -> Dict[str, Any]:
    """
    Executes real Tesseract OCR on base64 image and returns structured diagnostic result.
    Differentiates invalid image, timeout, unavailable binary, missing traineddata, and generic OCR errors.
    """
    if not image_b64:
        return {
            "extracted_text": "",
            "status": "empty_input",
            "message": "No screenshot image provided.",
            "ocr_engine_available": False,
            "available_languages": []
        }

    # Decode and validate image
    try:
        if "," in image_b64:
            image_b64 = image_b64.split(",", 1)[1]

        image_bytes = base64.b64decode(image_b64)
        raw_image = Image.open(io.BytesIO(image_bytes))
    except Exception as img_err:
        logger.warning(f"Corrupted/invalid image decode error: {img_err}")
        return {
            "extracted_text": "",
            "status": "invalid_image",
            "message": "Unable to read this image.",
            "ocr_engine_available": False,
            "available_languages": []
        }

    try:
        # Fast Visual Pre-Check (< 5ms blank image detection)
        if is_blank_image(raw_image):
            return {
                "extracted_text": "",
                "status": "no_text_found",
                "message": "⚠️ No readable text detected in this image.",
                "ocr_engine_available": True,
                "available_languages": []
            }

        # Fast Image Optimization (max 1200px)
        processed_image = optimize_image_for_fast_ocr(raw_image)

        # Resolve Tesseract binary executable
        tess_executable = resolve_tesseract_binary()

        try:
            import pytesseract
        except ImportError:
            return {
                "extracted_text": "",
                "status": "ocr_engine_missing",
                "message": "Tesseract OCR engine is unavailable.",
                "ocr_engine_available": False,
                "available_languages": []
            }

        if not tess_executable:
            return {
                "extracted_text": "",
                "status": "ocr_engine_missing",
                "message": "Tesseract OCR engine is unavailable.",
                "ocr_engine_available": False,
                "available_languages": []
            }

        try:
            available_langs = pytesseract.get_languages(config="")
        except Exception as tess_err:
            logger.info(f"Tesseract binary language check error: {tess_err}")
            return {
                "extracted_text": "",
                "status": "ocr_engine_missing",
                "message": "Tesseract OCR engine is unavailable.",
                "ocr_engine_available": False,
                "available_languages": []
            }

        # Language selection
        regional_code = LANG_MAP.get(preferred_lang, "eng")
        lang_config = f"eng+{regional_code}" if regional_code != "eng" else "eng"

        missing_langs = [l for l in lang_config.split("+") if l not in available_langs]
        if missing_langs:
            missing_str = ", ".join(missing_langs)
            if "eng" in available_langs:
                try:
                    text = pytesseract.image_to_string(processed_image, lang="eng", timeout=10)
                    return {
                        "extracted_text": text.strip(),
                        "status": "partial_language_missing",
                        "message": f"Tesseract language pack for '{missing_str}' is missing. Processed using English OCR.",
                        "ocr_engine_available": True,
                        "available_languages": available_langs
                    }
                except Exception:
                    pass

            return {
                "extracted_text": "",
                "status": "traineddata_missing",
                "message": f"Tesseract OCR language pack '{missing_str}' is not installed.",
                "ocr_engine_available": True,
                "available_languages": available_langs
            }

        # Construct safe timeout tuple supported by installed pytesseract version
        TimeoutExceptions = (subprocess.TimeoutExpired, TimeoutError, RuntimeError)
        if hasattr(pytesseract, 'TesseractTimeoutError'):
            TimeoutExceptions = TimeoutExceptions + (pytesseract.TesseractTimeoutError,)

        # Execute OCR with timeout
        try:
            extracted_text = pytesseract.image_to_string(
                processed_image,
                lang=lang_config,
                timeout=10
            ).strip()
        except TimeoutExceptions:
            return {
                "extracted_text": "",
                "status": "ocr_timeout",
                "message": "OCR is taking longer than expected. Please try a smaller or clearer screenshot.",
                "ocr_engine_available": True,
                "available_languages": available_langs
            }
        except Exception as tess_run_err:
            logger.error(f"Tesseract execution error: {tess_run_err}")
            return {
                "extracted_text": "",
                "status": "error",
                "message": "An error occurred during OCR text extraction. Please enter text manually.",
                "ocr_engine_available": True,
                "available_languages": available_langs
            }

        # Case A: No readable text
        if not extracted_text:
            return {
                "extracted_text": "",
                "status": "no_text_found",
                "message": "⚠️ No readable text detected in this screenshot.",
                "ocr_engine_available": True,
                "available_languages": available_langs
            }

        # Case C: Garbage OCR text
        if is_ocr_text_garbage(extracted_text):
            return {
                "extracted_text": extracted_text,
                "status": "garbage_text",
                "message": "⚠️ The extracted text doesn't appear readable or meaningful.",
                "ocr_engine_available": True,
                "available_languages": available_langs
            }

        # Case E: Valid OCR Text Extracted
        return {
            "extracted_text": extracted_text,
            "status": "success",
            "message": "Text extracted successfully from screenshot.",
            "ocr_engine_available": True,
            "available_languages": available_langs
        }

    except Exception as e:
        logger.error(f"Generic OCR processing exception: {e}")
        return {
            "extracted_text": "",
            "status": "error",
            "message": "An error occurred during OCR text extraction. Please enter text manually.",
            "ocr_engine_available": False,
            "available_languages": []
        }

def extract_text_from_image_b64(image_b64: str, preferred_lang: str = "English") -> str:
    """Convenience helper returning extracted text string."""
    res = process_ocr_with_diagnostics(image_b64, preferred_lang)
    return res.get("extracted_text", "")

extract_ocr_from_image_b64 = process_ocr_with_diagnostics
