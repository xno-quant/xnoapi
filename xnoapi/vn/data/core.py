
import time, random, requests

DEFAULT_TIMEOUT = 25

def _ua(source="vietmarket"):
    return {
        "User-Agent": f"{source}/1.0 (+https://example.local)",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://example.local",
        "Referer": "https://example.local/",
    }

def send_request(url, method="GET", headers=None, params=None, payload=None,
                 retries=2, backoff=(0.6, 1.2), timeout=DEFAULT_TIMEOUT):
    h = _ua()
    if headers:
        h.update(headers)
    for attempt in range(retries + 1):
        try:
            if method.upper() == "GET":
                r = requests.get(url, headers=h, params=params, timeout=timeout)
            else:
                r = requests.post(url, headers=h, params=params, json=payload, timeout=timeout)
            r.raise_for_status()
            if "application/json" in r.headers.get("Content-Type", ""):
                return r.json()
            return r.text
        except Exception:
            if attempt >= retries:
                raise
            time.sleep(random.uniform(*backoff))
