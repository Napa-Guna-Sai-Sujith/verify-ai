import sys
import os
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

def download_lang(lang_code):
    url = f"https://github.com/tesseract-ocr/tessdata_fast/raw/main/{lang_code}.traineddata"
    tessdata_dir = r"C:\Users\K R Sravani\Tesseract-OCR\tessdata"
    dest = os.path.join(tessdata_dir, f"{lang_code}.traineddata")

    print(f"Downloading {lang_code}.traineddata from {url}...")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"[OK] {lang_code}.traineddata downloaded successfully ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"[ERROR] Failed to download {lang_code}:", e)

def main():
    languages = ["kan", "tel", "tam", "hin"]
    for lang in languages:
        download_lang(lang)

if __name__ == "__main__":
    main()
