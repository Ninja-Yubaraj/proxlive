import os
import json
import time

from loader import load_proxies
from checker import check_proxy
from utils import run_threads


# ===================== CONFIG =====================
INPUT_FILE = "proxies.txt"

OUTPUT_DIR = "output"
TXT_OUTPUT = "working.txt"
JSON_OUTPUT = "working.json"
# =================================================


def main():
    proxies = load_proxies(INPUT_FILE)

    print(f"[+] Loaded {len(proxies)} proxies")

    results = run_threads(check_proxy, proxies)

    working = []

    for proxy, (status, data) in results:
        if status:
            print(f"[✔] Working: {proxy}")
            working.append({
                "proxy": proxy,
                "response": data
            })
        else:
            print(f"[✘] Dead: {proxy}")

    # ===================== OUTPUT HANDLING =====================

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Timestamped filenames
    timestamp = int(time.time())

    txt_path = os.path.join(OUTPUT_DIR, f"working_{timestamp}.txt")
    json_path = os.path.join(OUTPUT_DIR, f"working_{timestamp}.json")

    # Save TXT
    with open(txt_path, "w") as f:
        for p in working:
            f.write(p["proxy"] + "\n")

    # Save JSON
    with open(json_path, "w") as f:
        json.dump(working, f, indent=2)

    # ==========================================================

    print(f"\n[+] Working proxies: {len(working)}")
    print(f"[+] Saved TXT  -> {txt_path}")
    print(f"[+] Saved JSON -> {json_path}")


if __name__ == "__main__":
    main()
