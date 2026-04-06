import json


def load_txt(file_path):
    proxies = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                proxies.append(line)
    return proxies


def load_json(file_path):
    proxies = []
    with open(file_path, "r") as f:
        data = json.load(f)
        for entry in data:
            proxies.append(entry["proxy"])
    return proxies


def load_proxies(file_path):
    if file_path.endswith(".json"):
        return load_json(file_path)
    return load_txt(file_path)
