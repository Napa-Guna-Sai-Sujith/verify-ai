import sys
import os
import io
import json
import base64
import time
from PIL import Image, ImageDraw, ImageFont
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

API_URL = "http://127.0.0.1:8000/api/analyze"
OCR_URL = "http://127.0.0.1:8000/api/ocr"

def create_sample_image(text, width=800, height=300):
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 30)
    except Exception:
        font = ImageFont.load_default()
    draw.text((30, 100), text, fill=(0, 0, 0), font=font)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def run_ocr_test(name, b64_img, pref_lang="English"):
    t0 = time.time()
    req = urllib.request.Request(
        OCR_URL,
        data=json.dumps({"image_b64": b64_img, "preferred_language": pref_lang}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    elapsed = time.time() - t0
    data = json.loads(res_raw)
    print(f"[{name}] OCR Time: {elapsed:.3f}s | Status: {data.get('status')} | Text: {repr(data.get('extracted_text', '')[:40])}")
    return data

def run_analyze_test(name, text, pref_lang="English"):
    t0 = time.time()
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"text": text, "preferred_language": pref_lang}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_raw = urllib.request.urlopen(req).read().decode('utf-8')
    elapsed = time.time() - t0
    data = json.loads(res_raw)
    print(f"[{name}] Analyze Time: {elapsed:.3f}s | Topic: {data.get('claim_topic')} | Assessment: {data.get('assessment')} | Score: {data.get('trust_score')} | Sources: {len(data.get('sources', []))}")
    return data

def main():
    print("==================================================")
    print("RUNNING PART 19 TEST SUITE (10 CASES)")
    print("==================================================")

    # TEST 1: Short English message screenshot
    b64_1 = create_sample_image("Government scheme announced 10000 rupees for students.")
    res_1 = run_ocr_test("TEST 1 (English Screenshot)", b64_1)

    # TEST 2: Telugu WhatsApp screenshot
    b64_2 = create_sample_image("ప్రభుత్వం విద్యార్థులకు ఉచితంగా 10000 రూపాయిలు ప్రకటించింది.")
    res_2 = run_ocr_test("TEST 2 (Telugu Screenshot)", b64_2, "Telugu")

    # TEST 3: Kannada message screenshot
    b64_3 = create_sample_image("ಸರ್ಕಾರವು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ 10000 ರೂಪಾಯಿ ನೀಡಲು ಘೋಷಿಸಿದೆ.")
    res_3 = run_ocr_test("TEST 3 (Kannada Screenshot)", b64_3, "Kannada")

    # TEST 4: Blank Image (Visual pre-check < 5ms)
    img_blank = Image.new('RGB', (800, 600), color=(255, 255, 255))
    buf = io.BytesIO()
    img_blank.save(buf, format='PNG')
    b64_4 = base64.b64encode(buf.getvalue()).decode('utf-8')
    res_4 = run_ocr_test("TEST 4 (Blank Image)", b64_4)

    # TEST 5: Phone Settings Screenshot (Irrelevant UI)
    run_analyze_test("TEST 5 (Phone Settings)", "Settings Wi-Fi Bluetooth Battery 85% 12:45 PM")

    # TEST 6: Blank Text
    run_analyze_test("TEST 6 (Emojis Noise)", "😂😂😂😂")

    # TEST 7: Random OCR Noise
    run_analyze_test("TEST 7 (Random Symbols)", "asdfjkl; @#$% ^&*()")

    # TEST 8: Student Scheme Claim
    run_analyze_test("TEST 8 (Student Claim)", "Government has announced ₹10,000 for every student this month.")

    # TEST 9: Weather Claim
    run_analyze_test("TEST 9 (Weather Claim)", "School will remain closed tomorrow due to heavy rain.")

    # TEST 10: Medical Claim
    run_analyze_test("TEST 10 (Medical Claim)", "This medicine completely cures diabetes.")

    print("\n==================================================")
    print("ALL 10 TESTS COMPLETED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    main()
