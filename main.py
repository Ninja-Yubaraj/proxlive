from loader import load_proxies
from checker import check_proxy
from utils import run_threads
import json


INPUT_FILE = "proxies.txt"


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

    # Save TXT
    with open("output/working.txt", "w") as f:
        for p in working:
            f.write(p["proxy"] + "\n")

    # Save JSON
    with open("output/working.json", "w") as f:
        json.dump(working, f, indent=2)

    print(f"\n[+] Working proxies: {len(working)}")


if __name__ == "__main__":
    main()
