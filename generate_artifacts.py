import os
import sys
import zipfile
from services.presentation_gen import create_business_case_deck

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def build_all():
    print("[1/2] Generating 10-Slide Business Case Presentation...")
    pptx_path = os.path.join(BASE_DIR, "Business_Case_Presentation.pptx")
    create_business_case_deck(pptx_path)
    print(f"      Saved presentation to: {pptx_path}")

    print("[2/2] Packaging Submission ZIP File...")
    zip_path = os.path.join(BASE_DIR, "Project_Udyam_Digital_Airtel_SYNC.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    ignored_dirs = {"extracted_input", ".git", "__pycache__", ".vscode", "tmp"}
    ignored_exts = {".pyc", ".zip"}

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith('.')]
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in ignored_exts and f == "Project_Udyam_Digital_Airtel_SYNC.zip":
                    continue
                if ext == ".pyc":
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                z.write(full_path, rel_path)
                file_count += 1

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"      Packed {file_count} files into: {zip_path} ({size_mb:.2f} MB)")
    print("\nSUCCESS! All hackathon deliverables generated and packaged.")

if __name__ == "__main__":
    build_all()
