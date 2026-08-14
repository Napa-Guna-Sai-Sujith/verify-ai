import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

print("==================================================")
print("RUNNING FINAL CLASSIFICATION & RELEVANCE TESTS (10 CASES)")
print("==================================================")

rel_tests = [
    ("TEST 1 (Greeting)", "Hello, have a wonderful day!", "NOT RELEVANT"),
    ("TEST 2 (Emojis)", "😂😂😂😂", "NOT RELEVANT"),
    ("TEST 3 (Phone Settings)", "Settings Wi-Fi Bluetooth", "NOT RELEVANT"),
    ("TEST 4 (CTA Only)", "Share this immediately!", "NOT RELEVANT"),
    ("TEST 5 (CTA + Claim)", "Share this immediately to receive ₹15,000 from the government.", "RELEVANT"),
    ("TEST 6 (Health Claim)", "This medicine cures every disease.", "RELEVANT"),
    ("TEST 7 (Student Grant)", "Government has announced ₹15,000 for every student this month.", "RELEVANT"),
]

for name, text, expected in rel_tests:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"text": text, "preferred_language": "English"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res_raw)
    
    assessment = data.get('assessment')
    score = data.get('trust_score')
    sources_cnt = len(data.get('sources', []))
    
    is_not_rel = score is None or "NOT RELEVANT" in assessment
    actual = "NOT RELEVANT" if is_not_rel else "RELEVANT"
    
    print(f"[{name}] Expected: {expected} | Actual: {actual} | Assessment: {assessment} | Score: {score} | Sources: {sources_cnt}")

print("\n==================================================")
print("RUNNING URL ANALYSIS TESTS (5 CASES)")
print("==================================================")

url_tests = [
    ("URL TEST 1 (Official)", "Government scholarship announced. Details: https://pib.gov.in/PressReleasePage.aspx?PRID=123456", "TRUSTED"),
    ("URL TEST 2 (Malformed)", "Apply here http://https://pib-gov-scheme..com", "INVALID"),
    ("URL TEST 3 (Lookalike)", "Government ₹15,000 scholarship apply now http://pib-government-scholarship-scheme.top/claim", "SUSPICIOUS"),
    ("URL TEST 4 (Unknown)", "Check this update: https://some-random-local-blog-site.com/post", "UNVERIFIED"),
    ("URL TEST 5 (Shortened)", "Claim money now: https://bit.ly/3xXyZ12", "UNVERIFIED"),
]

for name, text, expected_status in url_tests:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"text": text, "preferred_language": "English"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res_raw)
    
    url_check = data.get('url_check')
    actual_status = url_check.get('status') if url_check else "NO_URL_CHECK"
    label = url_check.get('status_label') if url_check else ""
    reason = url_check.get('reason') if url_check else ""
    
    print(f"[{name}] Expected: {expected_status} | Actual: {actual_status} | Label: {label}")
    print(f"  └ Reason: {reason}\n")

print("==================================================")
print("ALL CLASSIFICATION & URL TESTS COMPLETED!")
print("==================================================")
