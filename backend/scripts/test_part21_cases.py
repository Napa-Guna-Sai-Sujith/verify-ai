import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

tests = [
    {
        "name": "TEST 1: Telugu input + Kannada preference",
        "input": "ప్రభుత్వం కొత్తగా విద్యార్థుల కోసం ₹15,000 ఆర్థిక సహాయ పథకాన్ని ప్రకటించింది.",
        "pref": "Kannada",
        "expected_detected": "Telugu",
        "expected_claim_script": "Telugu"
    },
    {
        "name": "TEST 2: Kannada input + Telugu preference",
        "input": "ಸರ್ಕಾರವು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ₹15,000 ಆರ್ಥಿಕ ನೆರವು ನೀಡಲು ನೂತನ ಯೋಜನೆ ಘೋಷಿಸಿದೆ.",
        "pref": "Telugu",
        "expected_detected": "Kannada",
        "expected_claim_script": "Kannada"
    },
    {
        "name": "TEST 3: Tamil input + Hindi preference",
        "input": "மாணவர்களுக்கு ரூபாய் 15,000 கல்வி உதவித்தொகை திட்டத்தை அரசு அறிவித்துள்ளது.",
        "pref": "Hindi",
        "expected_detected": "Tamil",
        "expected_claim_script": "Tamil"
    },
    {
        "name": "TEST 4: English input + Telugu preference",
        "input": "Government has announced ₹15,000 scheme for every student.",
        "pref": "Telugu",
        "expected_detected": "English",
        "expected_claim_script": "English"
    }
]

print("==================================================")
print("RUNNING PART 21 LANGUAGE SEPARATION TESTS (4 CASES)")
print("==================================================")

for t in tests:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({
            "text": t["input"],
            "preferred_language": t["pref"]
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res_raw)
    
    print(f"\n=== {t['name']} ===")
    print(f"Input Text           : {t['input']}")
    print(f"Detected Language    : {data.get('detected_language')}")
    print(f"Response Language    : {data.get('preferred_language')}")
    claims_list = data.get('claims') or []
    print(f"Extracted Claim #1   : {claims_list[0] if claims_list else '(none - claim extraction removed by design)'}")
    print(f"Claim Topic Internal : {data.get('claim_topic')}")
    print(f"Assessment Label     : {data.get('assessment')}")
    print(f"Explanation (snippet): {repr(data.get('explanation', '')[:80])}")

print("\n==================================================")
print("PART 21 TESTS COMPLETED!")
print("==================================================")
