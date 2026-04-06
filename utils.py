from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def run_threads(func, items, max_workers=50):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func, item): item for item in items}

        for future in tqdm(as_completed(futures), total=len(items)):
            results.append((futures[future], future.result()))

    return results
