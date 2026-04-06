import requests

TEST_URL = "http://httpbin.org/ip"


def check_proxy(proxy, timeout=5):
    try:
        proxies = {
            "http": proxy,
            "https": proxy,
        }

        response = requests.get(
            TEST_URL,
            proxies=proxies,
            timeout=timeout,
        )

        if response.status_code == 200:
            return True, response.json()

    except Exception:
        pass

    return False, None
