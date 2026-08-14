import sys
import os
import urllib.request
import subprocess

def main():
    url = 'https://github.com/mcmilk/7-Zip-zstd/releases/download/v26.02-v1.5.7-R2/7z26.02-zstd-x64.exe'
    dest_7z = r'C:\Users\K R Sravani\OneDrive\Desktop\VerityAI\7z-installer.exe'

    if not os.path.exists(dest_7z):
        print("Downloading 7-Zip x64 executable...")
        urllib.request.urlretrieve(url, dest_7z)
        print("Downloaded size:", os.path.getsize(dest_7z))

    # Extract 7z-installer using 7zr
    extract_7z_dir = r'C:\Users\K R Sravani\OneDrive\Desktop\VerityAI\7z-bin'
    os.makedirs(extract_7z_dir, exist_ok=True)

    print("Unpacking 7z installer using 7zr.exe...")
    subprocess.run([r'C:\Users\K R Sravani\OneDrive\Desktop\VerityAI\7zr.exe', 'x', dest_7z, f'-o{extract_7z_dir}', '-y'])

    z_exe = os.path.join(extract_7z_dir, '7z.exe')
    print("7z.exe exists:", os.path.exists(z_exe))

    if os.path.exists(z_exe):
        tess_out = r'C:\Users\K R Sravani\Tesseract-OCR'
        setup_file = r'C:\Users\K R Sravani\OneDrive\Desktop\VerityAI\tesseract-setup.exe'
        print("Extracting Tesseract NSIS setup using 7z.exe...")
        res = subprocess.run([z_exe, 'x', setup_file, f'-o{tess_out}', '-y'], capture_output=True, text=True)
        print("7z return code:", res.returncode)
        
        tess_exe = os.path.join(tess_out, 'tesseract.exe')
        print("Tesseract binary exists:", os.path.exists(tess_exe), "Path:", tess_exe)

if __name__ == "__main__":
    main()
