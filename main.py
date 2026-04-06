import os
import json
import time

from loader import load_proxies
from checker import check_proxy
from utils import run_threads


# ===================== CONFIG =====================
INPUT_FILE = "proxies.json"  # or proxies.txt
OUTPUT_DIR = "output"
# =================================================


def main():
    data, file_type = load_proxies(INPUT_FILE)

    print(f"[+] Loaded {len(data)} proxies ({file_type})")

    # ===================== PREPARE =====================

    if file_type == "txt":
        proxies = data
        proxy_map = {p: p for p in proxies}

    else:  # json
        proxies = [entry["proxy"] for entry in data]
        proxy_map = {entry["proxy"]: entry for entry in data}

    # =================================================

    results = run_threads(check_proxy, proxies)

    working = []

    for proxy, (status, response) in results:
        if status:
            print(f"[✔] Working: {proxy}")

            if file_type == "txt":
                working.append(proxy)

            else:  # json
                # Preserve original structure
                entry = proxy_map[proxy]
                working.append(entry)

        else:
            print(f"[✘] Dead: {proxy}")

    # ===================== OUTPUT =====================

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = int(time.time())

    if file_type == "txt":
        output_path = os.path.join(OUTPUT_DIR, f"working_{timestamp}.txt")

        with open(output_path, "w") as f:
            for proxy in working:
                f.write(proxy + "\n")

    else:  # json
        output_path = os.path.join(OUTPUT_DIR, f"working_{timestamp}.json")

        with open(output_path, "w") as f:
            json.dump(working, f, indent=2)

    # ==================================================

    print(f"\n[+] Working proxies: {len(working)}")
    print(f"[+] Saved -> {output_path}")


if __name__ == "__main__":
    main()
