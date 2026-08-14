import sys
import os
import base64
from io import BytesIO
from PIL import Image
from fastapi.testclient import TestClient

# Ensure app package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.services.language_service import detect_language
from app.services.ai_service import calculate_dynamic_trust_score
from app.services.claim_service import is_content_relevant, classify_claim_topic, extract_claims
from app.services.verification_service import is_generic_homepage, evaluate_evidence_status

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "Verity AI" in data["project"]

def test_five_different_claim_topics():
    # Test A: Government Financial/Student Claim
    text_a = "Government has announced ₹10,000 for every student."
    topic_a = classify_claim_topic(text_a, [text_a])
    assert topic_a in ["Education", "Financial / Scheme", "Government / Public Policy"]

    # Test B: Weather / School Closure Claim
    text_b = "Schools in Bengaluru will remain closed tomorrow due to heavy rain."
    topic_b = classify_claim_topic(text_b, [text_b])
    assert topic_b == "Weather / Advisory"

    # Test C: Medical / Health Claim
    text_c = "This medicine completely cures diabetes."
    topic_c = classify_claim_topic(text_c, [text_c])
    assert topic_c == "Health / Medical"

    # Test D: Financial Scam / Viral Message
    text_d = "Forward this message immediately to receive ₹5,000."
    topic_d = classify_claim_topic(text_d, [text_d])
    assert topic_d == "Financial Scam / Viral"

    # Test E: Science / Astronomy Claim
    text_e = "The moon will be visible during the daytime tomorrow."
    topic_e = classify_claim_topic(text_e, [text_e])
    assert topic_e == "Science / Astronomy"

    # Topics MUST be different across different domains
    topics = {topic_a, topic_b, topic_c, topic_d, topic_e}
    assert len(topics) >= 4

def test_irrelevant_content_detection():
    assert is_content_relevant("😂😂😂😂") is False
    assert is_content_relevant("12:45 PM") is False
    assert is_content_relevant("Home Search Settings Profile") is False
    assert is_content_relevant("hello") is False

    res = client.post("/api/analyze", json={"text": "😂😂😂😂", "preferred_language": "English"})
    assert res.status_code == 200
    data = res.json()
    assert data["assessment"] == "NOT RELEVANT"
    assert data["trust_score"] is None
    assert data["sources"] == []

def test_multilingual_outputs_all_five_languages():
    msg = "This medicine completely cures diabetes."
    languages = ["English", "Kannada", "Telugu", "Tamil", "Hindi"]

    for lang in languages:
        payload = {
            "text": msg,
            "preferred_language": lang
        }
        response = client.post("/api/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["preferred_language"] == lang
        assert data["claim_topic"] == "Health / Medical"
        assert len(data["explanation"]) > 10

def test_generic_homepage_and_evidence_status():
    assert is_generic_homepage("https://www.youtube.com/") is True
    assert is_generic_homepage("https://india.gov.in/") is True
    assert is_generic_homepage("https://pib.gov.in/PressReleasePage.aspx?PRID=123456") is False

    status, score = evaluate_evidence_status("PIB Fact Check: Diabetes Cure Claim Fake", "No evidence confirms diabetes cure pill", {"diabetes", "cure"}, "Health / Medical")
    assert status == "CONTRADICTS CLAIM"
    assert score >= 40

def test_ocr_endpoint():
    img = Image.new('RGB', (200, 100), color=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format='PNG')
    b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')

    response = client.post("/api/ocr", json={"image_b64": b64_str, "preferred_language": "Kannada"})
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "extracted_text" in data
