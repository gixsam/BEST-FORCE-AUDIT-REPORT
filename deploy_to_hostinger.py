"""
Hostinger Direct FTP / FTPS Deployment Script for https://audit.best-travel.ltd
Usage:
    python deploy_to_hostinger.py --host <FTP_HOST> --user <FTP_USER> --password <FTP_PASS> [--target-dir <DIR>]
Or configure environment variables:
    HOSTINGER_FTP_HOST=2.57.91.130
    HOSTINGER_FTP_USER=...
    HOSTINGER_FTP_PASS=...
    HOSTINGER_FTP_DIR=public_html
"""

import os
import sys
import ftplib
import argparse

LOCAL_FILES = ["index.html", ".htaccess", "robots.txt", "A4_Financial_Flow_Fraud_Catcher_Master.xlsx"]

def upload_to_ftp(host, user, password, remote_dir="public_html", port=21, use_tls=True):
    print(f"[*] Connecting to Hostinger FTP {host}:{port}...")
    
    ftp = None
    if use_tls:
        try:
            ftp = ftplib.FTP_TLS()
            ftp.connect(host, port, timeout=30)
            ftp.login(user, password)
            ftp.prot_p()
            print("[+] Connected securely with FTPS (TLS).")
        except Exception as e:
            print(f"[-] FTPS TLS negotiation failed ({e}), attempting standard FTP fallback...")
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=30)
            ftp.login(user, password)
            print("[+] Connected with standard FTP.")
    else:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=30)
        ftp.login(user, password)

    # Change to target directory
    print(f"[*] Navigating to target directory: {remote_dir}")
    try:
        ftp.cwd(remote_dir)
    except Exception as e:
        print(f"[!] Warning navigating to {remote_dir} ({e}), current directory: {ftp.pwd()}")

    # Upload each production file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    uploaded_count = 0
    for fname in LOCAL_FILES:
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            print(f"[-] Skipped missing file: {fname}")
            continue
        
        file_size = os.path.getsize(fpath)
        print(f"[*] Uploading {fname} ({file_size:,} bytes)...")
        with open(fpath, "rb") as fp:
            ftp.storbinary(f"STOR {fname}", fp)
        print(f"  [OK] Successfully uploaded {fname}")
        uploaded_count += 1

    ftp.quit()
    print(f"\n[SUCCESS] Deployed {uploaded_count} files directly to Hostinger!")
    print("Live Production URL: https://audit.best-travel.ltd")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hostinger Direct Deployment")
    parser.add_argument("--host", default=os.getenv("HOSTINGER_FTP_HOST", "2.57.91.130"))
    parser.add_argument("--user", default=os.getenv("HOSTINGER_FTP_USER"))
    parser.add_argument("--password", default=os.getenv("HOSTINGER_FTP_PASS"))
    parser.add_argument("--target-dir", default=os.getenv("HOSTINGER_FTP_DIR", "public_html"))
    args = parser.parse_args()

    if not args.user or not args.password:
        print("Error: Missing credentials.")
        print("Provide via command line arguments:")
        print("  python deploy_to_hostinger.py --user <FTP_USER> --password <FTP_PASS>")
        print("Or set environment variables: HOSTINGER_FTP_USER, HOSTINGER_FTP_PASS")
        sys.exit(1)

    upload_to_ftp(args.host, args.user, args.password, args.target_dir)
