import sys
import os
import urllib.request
import py7zr

def main():
    setup_file = r"C:\Users\K R Sravani\OneDrive\Desktop\VerityAI\tesseract-setup.exe"
    target_dir = r"C:\Users\K R Sravani\Tesseract-OCR"

    print("Opening setup file with py7zr...")
    try:
        with py7zr.SevenZipFile(setup_file, mode='r') as z:
            z.extractall(path=target_dir)
        print("SUCCESS! Extracted to:", target_dir)
        exe = os.path.join(target_dir, "tesseract.exe")
        print("Executable exists:", os.path.exists(exe))
    except Exception as e:
        print("py7zr error:", e)

if __name__ == "__main__":
    main()
