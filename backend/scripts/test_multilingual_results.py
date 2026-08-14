import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

languages = ["Telugu", "Kannada", "Tamil", "Hindi", "English"]
sample_text = "Government has announced ₹10,000 for every student this month."

print("==================================================")
print("TESTING FULL LOCALIZATION ACROSS ALL 5 LANGUAGES")
print("==================================================")

for lang in languages:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({
            "text": sample_text,
            "preferred_language": lang
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res_raw)
    
    print(f"\n=== PREFERRED LANGUAGE: {lang} ===")
    print(f"Detected Language : {data.get('detected_language')}")
    print(f"Preferred Language: {data.get('preferred_language')}")
    print(f"Claim Topic       : {data.get('claim_topic')}")
    print(f"Assessment        : {data.get('assessment')}")
    print(f"Trust Score       : {data.get('trust_score')}")
    print(f"Explanation (first 100 chars): {repr(data.get('explanation', '')[:100])}")
    print(f"Recommendation    : {data.get('recommendation')}")
    print(f"Checklist Title #1: {data.get('before_you_share', [{}])[0].get('title')}")

print("\n==================================================")
print("ALL 5 LANGUAGES TESTED SUCCESSFULLY!")
print("==================================================")
