import os
import json
import time
import argparse
from functools import partial

from .loader import load_proxies
from .checker import check_proxy
from .utils import run_threads


# ===================== CLI =====================

def parse_args():
    parser = argparse.ArgumentParser(
        description="proxlive - Fast proxy checker"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input file (.txt or .json)"
    )

    parser.add_argument(
        "-t", "--threads",
        type=int,
        default=50,
        help="Number of threads (default: 50)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Request timeout in seconds (default: 5)"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file (optional)"
    )

    return parser.parse_args()


# =================================================


def run():
    args = parse_args()

    INPUT_FILE = args.input
    THREADS = args.threads
    TIMEOUT = args.timeout
    OUTPUT_FILE = args.output

    # ===================== LOAD =====================

    if not os.path.exists(INPUT_FILE):
        print("[!] Input file not found")
        return

    data, file_type = load_proxies(INPUT_FILE)

    print(f"[+] Loaded {len(data)} proxies ({file_type})")

    # ===================== PREP =====================

    if file_type == "txt":
        proxies = data
        proxy_map = {p: p for p in proxies}

    else:  # json
        proxies = [entry["proxy"] for entry in data]
        proxy_map = {entry["proxy"]: entry for entry in data}

    # Bind timeout into checker
    check = partial(check_proxy, timeout=TIMEOUT)

    # ===================== RUN =====================

    results = run_threads(check, proxies, max_workers=THREADS)

    working = []

    for proxy, (status, response) in results:
        if status:
            if file_type == "txt":
                working.append(proxy)
            else:
                entry = proxy_map[proxy]
                working.append(entry)

    # ===================== OUTPUT =====================

    timestamp = int(time.time())

    # Decide extension based on input
    ext = "txt" if file_type == "txt" else "json"

    if OUTPUT_FILE:
        # Add extension if missing
        if not OUTPUT_FILE.endswith(f".{ext}"):
            output_path = f"{OUTPUT_FILE}.{ext}"
        else:
            output_path = OUTPUT_FILE
    else:
        # Default filename (UPDATED)
        output_path = f"proxies_{timestamp}.{ext}"

    # Create directory only if user specified a path
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Write output
    if file_type == "txt":
        with open(output_path, "w") as f:
            for proxy in working:
                f.write(proxy + "\n")

    else:  # json
        with open(output_path, "w") as f:
            json.dump(working, f, indent=2)

    # ==================================================

    print(f"\n[+] Working proxies: {len(working)}")
    print(f"[+] Saved -> {output_path}")


if __name__ == "__main__":
    run()
