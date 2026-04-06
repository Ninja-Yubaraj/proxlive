import requests

TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 5


def check_proxy(proxy):
    try:
        proxies = {
            "http": proxy,
            "https": proxy,
        }

        response = requests.get(
            TEST_URL,
            proxies=proxies,
            timeout=TIMEOUT,
        )

        if response.status_code == 200:
            return True, response.json()
    except Exception:
        pass

    return False, None
