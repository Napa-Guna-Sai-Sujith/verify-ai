import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

print("==================================================")
print("TESTING REWORKED SCREENSHOT & CONTENT PIPELINE (9 CASES)")
print("==================================================")

tests = [
    (
        "1. Standalone PUMA URL",
        "https://in.puma.com/in/en/lifestyle",
        "Standalone URL"
    ),
    (
        "2. PUMA URL + normal message",
        "Visit PUMA here: https://in.puma.com/in/en/lifestyle",
        "PUMA URL + CTA"
    ),
    (
        "3. Telugu misinformation message",
        "ప్రభుత్వం కొత్తగా విద్యార్థుల కోసం ₹15,000 ప్రకటించింది.",
        "Telugu Claim"
    ),
    (
        "4. Kannada misinformation message",
        "ಸರ್ಕಾರವು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ₹15,000 ಘೋಷಿಸಿದೆ.",
        "Kannada Claim"
    ),
    (
        "5. Random photograph / Noise",
        "random abc xyz 123",
        "OCR Noise"
    ),
    (
        "6. Phone settings screenshot",
        "Settings Wi-Fi Bluetooth Battery",
        "Phone UI Text"
    ),
    (
        "7. Share this immediately!",
        "Share this immediately!",
        "Spam Forwarding Language"
    ),
    (
        "8. Genuine factual claim",
        "This medicine completely cures diabetes.",
        "Medical Factual Claim"
    ),
    (
        "9. Screenshot containing claim + URL",
        "Government announced ₹15,000 for students. Apply here: https://example.com",
        "Claim + URL + CTA"
    )
]

for name, input_text, desc in tests:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"text": input_text, "preferred_language": "English"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res_raw)

    content_types = data.get('detected_content_types', [])
    claims = data.get('claims', [])
    url_check = data.get('url_check')
    score = data.get('trust_score')
    sources = data.get('sources', [])
    assessment = data.get('assessment')
    risk_indicators = data.get('risk_indicators', [])

    print(f"[{name}]")
    print(f"  Input Text: {input_text}")
    print(f"  Detected Content Types: {content_types}")
    print(f"  Extracted Claims: {claims}")
    print(f"  URL Check Status: {url_check.get('status') if url_check else 'None'}")
    print(f"  Risk Indicators: {risk_indicators}")
    print(f"  Assessment: {assessment}")
    print(f"  Trust Score: {score}")
    print(f"  Evidence Searches: {len(sources)}\n")

print("==================================================")
print("COMPLETED REWORKED SCREENSHOT PIPELINE TESTS")
print("==================================================")
