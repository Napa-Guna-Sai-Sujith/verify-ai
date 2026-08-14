import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

print("==================================================")
print("TESTING DASHBOARD STATISTICS CLASSIFICATION (7 CASES)")
print("==================================================")

tests = [
    (
        "TEST 1 (Trusted URL)",
        "https://in.puma.com/in/en/lifestyle",
        "URL-Only Trusted"
    ),
    (
        "TEST 2 (Unknown URL)",
        "https://unverified-domain-12345.org",
        "URL-Only Unverified"
    ),
    (
        "TEST 3 (Suspicious URL)",
        "https://puma-discount.top",
        "URL-Only Suspicious"
    ),
    (
        "TEST 4 (Factual Message - Insufficient Evidence)",
        "Government announced ₹15,000 for every student.",
        "Factual Needs Verification"
    ),
    (
        "TEST 5 (Factual Message - Supporting Evidence)",
        "ISRO launched Chandrayaan-3 lunar mission.",
        "Factual Supported"
    ),
    (
        "TEST 6 (Factual Message - Contradictory Evidence)",
        "This medicine completely cures diabetes.",
        "Factual Misleading"
    ),
    (
        "TEST 7 (Message + URL)",
        "Government announced ₹15,000 for students. Apply here: https://example.com",
        "Message + URL"
    )
]

def is_url_only_analysis(data):
    score = data.get('trust_score')
    url_check = data.get('url_check')
    url_checks = data.get('url_checks', [])
    content_types = data.get('detected_content_types', [])
    assessment = (data.get('assessment') or '').upper()

    if score is None and (url_check or url_checks):
        return True
    if 'URL' in content_types and 'MESSAGE_TEXT' not in content_types and 'FACTUAL_CLAIM' not in content_types:
        return True
    if any(k in assessment for k in ['VERIFIED / TRUSTED DOMAIN', 'UNVERIFIED URL', 'SUSPICIOUS LOOKALIKE LINK', 'INVALID URL LINK', 'TRUSTED DOMAIN', 'UNVERIFIED LINK']):
        return True
    return False

def is_not_relevant_analysis(data):
    assessment = (data.get('assessment') or '').upper()
    return any(k in assessment for k in ['NOT RELEVANT', 'సూక్తవాగిల్ల', 'సంబంధిత', 'प्रासंगिक नहीं'])

stats = {
    "total": 0,
    "supported": 0,
    "needsVerification": 0,
    "misleading": 0,
    "urlChecks": 0
}

for name, input_text, desc in tests:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"text": input_text, "preferred_language": "English"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(res_raw)

    is_url_only = is_url_only_analysis(data)
    is_not_rel = is_not_relevant_analysis(data)

    assessment = data.get('assessment', '')
    score = data.get('trust_score')

    prev_needs_verif = stats["needsVerification"]
    prev_supported = stats["supported"]
    prev_misleading = stats["misleading"]
    prev_url_checks = stats["urlChecks"]

    stats["total"] += 1

    if is_not_rel:
        category = "EXCLUDED (Not Relevant)"
    elif is_url_only:
        category = "URL CHECK ONLY (Excluded from Factual Stats)"
        stats["urlChecks"] += 1
    else:
        a_low = assessment.lower()
        if 'supported' in a_low or 'ದೃಢೀಕರಿಸಲಾಗಿದೆ' in a_low or 'నిర్ధారించబడింది' in a_low:
            category = "FACTUAL: Evidence Supported (+1 Supported)"
            stats["supported"] += 1
        elif 'misleading' in a_low or 'ತಪ್ಪಿಸುವ' in a_low or 'తప్పుదోవ' in a_low:
            category = "FACTUAL: Potentially Misleading (+1 Misleading)"
            stats["misleading"] += 1
        elif 'needs verification' in a_low or 'ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ' in a_low or 'ధృవీకరణ అవసరం' in a_low:
            category = "FACTUAL: Needs Verification (+1 Needs Verification)"
            stats["needsVerification"] += 1
        else:
            category = "UNRECOGNIZED (Excluded from Factual Stats)"

    print(f"[{name}]")
    print(f"  Input: {input_text}")
    print(f"  Assessment: {assessment} | Trust Score: {score}")
    print(f"  Is URL-Only Check: {is_url_only}")
    print(f"  Category for Dashboard: {category}")
    print(f"  Stats After Item -> Total: {stats['total']} | Supported: {stats['supported']} | Needs Verification: {stats['needsVerification']} | Misleading: {stats['misleading']} | Link Checks: {stats['urlChecks']}\n")

print("==================================================")
print("FINAL DASHBOARD STATISTICS VERIFICATION")
print(f"Total Verifications: {stats['total']}")
print(f"Factual Supported: {stats['supported']}")
print(f"Factual Needs Verification: {stats['needsVerification']}")
print(f"Factual Misleading: {stats['misleading']}")
print(f"URL Link Checks: {stats['urlChecks']}")
print("==================================================")
