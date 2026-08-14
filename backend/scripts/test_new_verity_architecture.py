import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

print("==================================================")
print("TESTING NEW VERITY AI ARCHITECTURE (8 CASES)")
print("==================================================")

tests = [
    (
        "TEST 1 (Standalone PUMA URL)",
        "https://in.puma.com/in/en/lifestyle",
        "Standalone PUMA URL"
    ),
    (
        "TEST 2 (PUMA URL + normal message)",
        "Visit PUMA here:\nhttps://in.puma.com/in/en/lifestyle",
        "PUMA URL + Text"
    ),
    (
        "TEST 3 (Direct Message)",
        "Government has announced ₹15,000 for every student.",
        "Direct Message"
    ),
    (
        "TEST 4 (Message + URL)",
        "Government has announced ₹15,000 for every student.\nApply here:\nhttps://example.com",
        "Message + URL"
    ),
    (
        "TEST 5 (Random Noise / Irrelevant)",
        "random abc xyz 123",
        "Noise"
    ),
    (
        "TEST 6 (Screenshot containing URL)",
        "https://in.puma.com/in/en/lifestyle",
        "OCR URL"
    ),
    (
        "TEST 7 (Screenshot containing message + URL)",
        "Government announced ₹15,000 for students. Apply here: https://example.com",
        "OCR Message + URL"
    ),
    (
        "TEST 8 (Multiple URLs)",
        "Check official site https://in.puma.com and store https://shop.adidas.co.in",
        "Multiple URLs"
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

    claims = data.get('claims', [])
    url_check = data.get('url_check')
    url_checks = data.get('url_checks', [])
    score = data.get('trust_score')
    sources = data.get('sources', [])
    assessment = data.get('assessment')
    risk_indicators = data.get('risk_indicators', [])

    has_bad_search = any("https://in" in (s.get('title', '') + s.get('url', '') + s.get('relevance', '')) for s in sources)

    print(f"[{name}]")
    print(f"  Input: {input_text}")
    print(f"  Extracted Claims: {claims} (Claim Analysis Removed: {len(claims) == 0})")
    print(f"  Primary URL Check Status: {url_check.get('status') if url_check else 'None'}")
    print(f"  URL Checks Count: {len(url_checks)}")
    print(f"  Assessment: {assessment}")
    print(f"  Trust Score: {score}")
    print(f"  Evidence Searches Count: {len(sources)}")
    print(f"  Bad 'https://in' Search Detected: {has_bad_search}\n")

print("==================================================")
print("COMPLETED NEW VERITY AI ARCHITECTURE TESTS")
print("==================================================")
