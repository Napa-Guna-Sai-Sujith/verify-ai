import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

print("==================================================")
print("TESTING URL SEPARATION & NO-FACTUAL-CLAIM VERIFICATION")
print("==================================================")

tests = [
    (
        "TEST A (Standalone PUMA URL)",
        "https://in.puma.com/in/en/lifestyle",
        "PUMA Standalone URL"
    ),
    (
        "TEST B (CTA + PUMA URL)",
        "Visit PUMA here: https://in.puma.com/in/en/lifestyle",
        "PUMA CTA + URL"
    ),
    (
        "TEST C (Claim + URL)",
        "Government scholarship available here: https://example.com/apply",
        "Scholarship Claim + URL"
    ),
    (
        "TEST D (URL with Query Params)",
        "https://www.example.com/page?id=123&category=test",
        "Query Params URL"
    ),
    (
        "TEST E (Multiple URLs)",
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
    score = data.get('trust_score')
    sources = data.get('sources', [])
    assessment = data.get('assessment')

    # Verify that evidence search NEVER searched for "https://in"
    has_bad_search = any("https://in" in (s.get('title', '') + s.get('url', '') + s.get('relevance', '')) for s in sources)

    print(f"[{name}]")
    print(f"  Input: {input_text}")
    print(f"  Extracted Claims: {claims} (Count: {len(claims)})")
    print(f"  URL Check Status: {url_check.get('status') if url_check else 'None'}")
    print(f"  URL Check Label: {url_check.get('status_label') if url_check else 'None'}")
    print(f"  Trust Score: {score}")
    print(f"  Evidence Sources Count: {len(sources)}")
    print(f"  Bad 'https://in' Search Detected: {has_bad_search}\n")

print("==================================================")
print("COMPLETED URL SEPARATION TESTS")
print("==================================================")
