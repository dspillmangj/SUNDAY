import os
import shutil
import zipfile
import hashlib
import json
import subprocess
from datetime import datetime

# --- Configuration ---
APP_FOLDER = "SUNDAY"
OUTPUT_ZIP = "SUNDAY_Update.zip"
LATEST_JSON = "latest.json"
VERSION = "1.2.1"
NOTES = "🎉 Added update check, version control, and hash validation."
DOWNLOAD_URL = "https://github.com/dspillmangj/SUNDAY/releases/latest/download/SUNDAY_Update.zip"
PUSH_TO_GITHUB = True  # Set to False if you don't want it to auto-push

# --- Step 1: Zip the project ---
def zip_app(source_dir, zip_filename):
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, start=source_dir)
                zipf.write(filepath, os.path.join(os.path.basename(source_dir), arcname))

# --- Step 2: Compute SHA-256 ---
def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

# --- Step 3: Update latest.json ---
def update_latest_json(version, url, hash_value, notes):
    latest = {
        "latest_version": version,
        "download_url": url,
        "sha256": hash_value,
        "notes": notes
    }
    with open(LATEST_JSON, 'w') as f:
        json.dump(latest, f, indent=4)
    print(f"✅ {LATEST_JSON} updated")

# --- Step 4 (Optional): GitHub Commit & Push ---
def git_commit_and_push():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Release v{VERSION} - {datetime.now().isoformat()}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("🚀 Changes pushed to GitHub.")

# --- Run All Steps ---
def main():
    print("📦 Zipping project...")
    zip_app(APP_FOLDER, OUTPUT_ZIP)

    print("🔐 Computing SHA-256...")
    hash_value = compute_sha256(OUTPUT_ZIP)

    print("📝 Updating latest.json...")
    update_latest_json(VERSION, DOWNLOAD_URL, hash_value, NOTES)

    if PUSH_TO_GITHUB:
        print("📤 Committing and pushing to GitHub...")
        git_commit_and_push()

    print("✅ Done. Your update package is ready.")

if __name__ == "__main__":
    main()