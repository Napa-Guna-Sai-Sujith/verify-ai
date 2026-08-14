import sys
import os
import urllib.request
import zipfile
import subprocess

def main():
    url = 'https://github.com/dscharrer/innoextract/releases/download/1.9/innoextract-1.9-windows.zip'
    dest_zip = r'C:\Users\K R Sravani\OneDrive\Desktop\VerityAI\innoextract.zip'
    extract_dir = r'C:\Users\K R Sravani\OneDrive\Desktop\VerityAI\innoextract'

    print("Downloading innoextract binary...")
    urllib.request.urlretrieve(url, dest_zip)
    print("Downloaded size:", os.path.getsize(dest_zip))

    with zipfile.ZipFile(dest_zip, 'r') as z:
        z.extractall(extract_dir)

    inno_exe = os.path.join(extract_dir, 'innoextract.exe')
    print("innoextract.exe exists:", os.path.exists(inno_exe))

    setup_file = r'C:\Users\K R Sravani\OneDrive\Desktop\VerityAI\tesseract-setup.exe'
    tesseract_out = r'C:\Users\K R Sravani\Tesseract-OCR'

    if os.path.exists(inno_exe) and os.path.exists(setup_file):
        print("Unpacking Tesseract installer using innoextract...")
        res = subprocess.run([inno_exe, '-e', setup_file, '-d', tesseract_out], capture_output=True, text=True)
        print("Unpack exit code:", res.returncode)
        print("Output:", res.stdout[:300])

        tess_exe = os.path.join(tesseract_out, 'app', 'tesseract.exe')
        if not os.path.exists(tess_exe):
            tess_exe = os.path.join(tesseract_out, 'tesseract.exe')
        print("Tesseract binary exists:", os.path.exists(tess_exe), "Path:", tess_exe)

if __name__ == "__main__":
    main()
