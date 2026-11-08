"""
Airtel Project Udyam Digital - 1-Click Startup Runner
Airtel SYNC Hackathon 2026 · Track A
"""
import os
import sys
import webbrowser
import threading
import time

def open_browser():
    time.sleep(1.5)
    url = "http://localhost:5000"
    print(f"\n[Airtel Udyam Digital] Opening Web Application at: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    print("=" * 70)
    print("    AIRTEL SYNC HACKATHON 2026 · PROJECT UDYAM DIGITAL")
    print("    Making Small Businesses Go Digital in One Sitting")
    print("=" * 70)

    # Verify python version
    print(f"[*] Python environment: {sys.version.split()[0]}")
    
    # Check data directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    if not os.path.exists(data_dir):
        print("[!] Warning: data directory not found at", data_dir)
    else:
        print(f"[*] Datasets verified at: {data_dir}")

    # Launch browser thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start Flask application
    from app import app
    print("\n[*] Starting Local Server on http://localhost:5000 (Press Ctrl+C to stop)...")
    app.run(host="0.0.0.0", port=5000, debug=False)
