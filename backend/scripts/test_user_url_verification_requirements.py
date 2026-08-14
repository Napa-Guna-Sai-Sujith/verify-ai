import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

print("==================================================")
print("VERITY AI — COMPREHENSIVE URL VERIFICATION TEST SUITE")
print("==================================================")

test_cases = [
    (
        "1. Programiz URL (Reachable HTTPS domain)",
        "https://www.programiz.com/python-programming/online-compiler/",
        "TRUSTED",
        "🟢 VERIFIED / TRUSTED DOMAIN"
    ),
    (
        "2. PUMA Regional Subdomain",
        "https://in.puma.com/in/en/lifestyle",
        "TRUSTED",
        "🟢 VERIFIED / TRUSTED DOMAIN"
    ),
    (
        "3. Legitimate Site with www",
        "https://www.geeksforgeeks.org/python-programming-language/",
        "TRUSTED",
        "🟢 VERIFIED / TRUSTED DOMAIN"
    ),
    (
        "4. Legitimate Regional / Store Subdomain",
        "https://shop.adidas.co.in/lifestyle",
        "TRUSTED",
        "🟢 VERIFIED / TRUSTED DOMAIN"
    ),
    (
        "5. Unknown but Valid Unreachable Domain",
        "https://unverified-domain-1234567.org",
        "UNVERIFIED",
        "🟡 UNKNOWN / UNVERIFIED URL"
    ),
    (
        "6. Malformed URL",
        "http://https://pib-gov-scheme..com",
        "INVALID",
        "⚠️ INVALID URL"
    ),
    (
        "7. Clear Lookalike / Impersonation Domain",
        "http://puma-discount-shoes.top/claim",
        "SUSPICIOUS",
        "🔴 SUSPICIOUS / POTENTIALLY MALICIOUS URL"
    )
]

passed_count = 0

for name, url_input, expected_status, expected_label in test_cases:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"text": url_input, "preferred_language": "English"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res_raw)

    url_check = data.get('url_check') or {}
    actual_status = url_check.get('status')
    actual_label = url_check.get('status_label')
    reason = url_check.get('reason')
    assessment = data.get('assessment')
    score = data.get('trust_score')
    sources = data.get('sources')

    is_pass = actual_status == expected_status and actual_label == expected_label
    if is_pass:
        passed_count += 1

    result_symbol = "✅ PASS" if is_pass else "❌ FAIL"

    print(f"[{name}] -> {result_symbol}")
    print(f"  Input URL:      {url_input}")
    print(f"  Expected Status:{expected_status} ({expected_label})")
    print(f"  Actual Status:  {actual_status} ({actual_label})")
    print(f"  Assessment:     {assessment}")
    print(f"  Trust Score:    {score} (Must be None for URL-only)")
    print(f"  Sources Count:  {len(sources)} (Must be 0 for URL-only)")
    print(f"  Reason:         {reason}\n")

print("==================================================")
print(f"SUMMARY: {passed_count} / {len(test_cases)} TESTS PASSED")
print("==================================================")

if passed_count == len(test_cases):
    print("🎉 ALL URL VERIFICATION TEST CASES PASSED SUCCESSFULLY!")
else:
    sys.exit(1)
