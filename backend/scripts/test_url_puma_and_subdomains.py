import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"

print("==================================================")
print("RUNNING PUMA & SUBDOMAIN URL VERIFICATION TESTS")
print("==================================================")

url_cases = [
    (
        "PUMA Regional Subdomain",
        "Buy PUMA products here: https://in.puma.com/in/en/lifestyle",
        "TRUSTED",
        "https://in.puma.com/in/en/lifestyle"
    ),
    (
        "PUMA www Subdomain",
        "Official PUMA site: https://www.puma.com/in/en",
        "TRUSTED",
        "https://www.puma.com/in/en"
    ),
    (
        "Brand Regional/Product Subdomain",
        "Check Adidas store: https://shop.adidas.co.in/lifestyle",
        "TRUSTED",
        "https://shop.adidas.co.in/lifestyle"
    ),
    (
        "Unknown Valid Domain",
        "Read this post: https://some-random-local-blog-site.com/post",
        "UNVERIFIED",
        "https://some-random-local-blog-site.com/post"
    ),
    (
        "Malformed URL",
        "Click link http://https://pib-gov-scheme..com",
        "INVALID",
        "http://https://pib-gov-scheme..com"
    ),
    (
        "Lookalike Impersonation Domain",
        "PUMA 90% discount sale claim here http://puma-discount-shoes.top/claim",
        "SUSPICIOUS",
        "http://puma-discount-shoes.top/claim"
    )
]

for name, text, expected_status, test_url in url_cases:
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

    print(f"[{name}]")
    print(f"  URL: {test_url}")
    print(f"  Expected Status: {expected_status} | Actual Status: {actual_status}")
    print(f"  Label: {label}")
    print(f"  Reason: {reason}\n")

print("==================================================")
print("COMPLETED PUMA & SUBDOMAIN URL VERIFICATION TESTS")
print("==================================================")
