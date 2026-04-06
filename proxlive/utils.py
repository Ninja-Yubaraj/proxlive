from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import sys


def run_threads(func, items, max_workers=50):
    results = []

    stats = {
        "total": len(items),
        "checked": 0,
        "working": 0,
        "dead": 0,
        "start_time": time.time()
    }

    lock = threading.Lock()

    def update_stats(status):
        with lock:
            stats["checked"] += 1
            if status:
                stats["working"] += 1
            else:
                stats["dead"] += 1

            # Calculate speed
            elapsed = time.time() - stats["start_time"]
            speed = stats["checked"] / elapsed if elapsed > 0 else 0

            # Live print (single line)
            sys.stdout.write(
                f"\r[Checked: {stats['checked']}/{stats['total']}] "
                f"[✔ {stats['working']}] "
                f"[✘ {stats['dead']}] "
                f"[⚡ {speed:.2f} p/s]"
            )
            sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func, item): item for item in items}

        for future in as_completed(futures):
            proxy = futures[future]
            result = future.result()

            status = result[0]
            update_stats(status)

            results.append((proxy, result))

    print()  # move to next line after progress bar
    return results
