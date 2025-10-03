from __future__ import annotations

import urllib.request
import urllib.error
from typing import Iterable, Optional


class APIKeyNotSetError(ValueError):
    """Raised when API key has not been set."""


class InvalidAPIKeyError(ValueError):
    """Raised when API key is invalid or unauthorized."""


class Config:
    """
    Configuration class for managing the API key and providing the API endpoint.

    Attributes:
        _api_key (str | None): The stored API key. Defaults to None.
    """

    _api_key: Optional[str] = None

    # ───────────────────────── Public API ─────────────────────────

    @classmethod
    def set_api_key(
        cls,
        apikey: str,
        *,
        verify: bool = True,
        header: str = "x-api-key",
        scheme: Optional[str] = None,
        # Thêm route bảo vệ thật sự ở cuối để xác thực chắc chắn:
        probe_paths: Iterable[str] = ("/v1/ping", "/ping", "/healthz", "/status", "/", "/list-liquid-asset"),
        timeout: float = 5.0,
    ):
        """
        Set the API key. If `verify=True` (default), the key is validated online
        BEFORE being saved. If invalid, raise and DO NOT save the key.

        Raises:
            ValueError: Empty key.
            InvalidAPIKeyError: Key sai/unauthorized.
            ConnectionError: Lỗi mạng/timeout/DNS.
        """
        if not isinstance(apikey, str) or not apikey.strip():
            raise ValueError("API key must be a non-empty string.")
        candidate = apikey.strip()

        if verify:
            # Xác thực TRƯỚC khi lưu để tránh lưu key sai
            cls._probe_api_key(candidate, header=header, scheme=scheme, probe_paths=probe_paths, timeout=timeout)

        # Ok -> lưu
        cls._api_key = candidate

    @classmethod
    def get_api_key(cls) -> str:
        """
        Retrieve the currently set API key.

        Raises:
            APIKeyNotSetError: If the API key has not been set.
        """
        if cls._api_key is None:
            raise APIKeyNotSetError("API key is not set. Use client(apikey=...) to set it.")
        return cls._api_key

    @classmethod
    def get_link(cls) -> str:
        """Return the API base URL."""
        return "https://d16sdkoet71cxx.cloudfront.net"

    # ───────────────────────── Internals ─────────────────────────

    @classmethod
    def _build_headers_for_key(cls, key: str, *, header: str = "x-api-key", scheme: Optional[str] = None) -> dict:
        """
        Build headers using a PROVIDED key (không phụ thuộc vào get_api_key()).
        Giúp probe trước khi lưu key.
        """
        if header.lower() == "authorization":
            value = f"{scheme} {key}".strip() if scheme else key
            return {"Authorization": value}
        return {header: key}

    @classmethod
    def _probe_api_key(
        cls,
        key: str,
        *,
        header: str = "x-api-key",
        scheme: Optional[str] = None,
        probe_paths: Iterable[str] = ("/v1/ping", "/ping", "/healthz", "/status", "/"),
        timeout: float = 5.0,
    ) -> bool:
        """
        Validate a PROVIDED API key (không đòi hỏi key đã được set).
        - 2xx: hợp lệ -> return True
        - 401/403: raise InvalidAPIKeyError
        - 404/405/...: thử path kế tiếp
        - Lỗi mạng: raise ConnectionError
        """
        base = cls.get_link().rstrip("/")
        headers = cls._build_headers_for_key(key, header=header, scheme=scheme)

        for path in probe_paths:
            url = base + (path if path.startswith("/") else f"/{path}")
            req = urllib.request.Request(url=url, method="GET", headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    code = getattr(resp, "status", 200)
                    if 200 <= code < 300:
                        return True
            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    raise InvalidAPIKeyError(f"Invalid API key (HTTP {e.code}) for {url}") from e
                # 404/405/...: thử path tiếp theo
                continue
            except urllib.error.URLError as e:
                raise ConnectionError(f"Failed to validate API key against {url}: {e}") from e

        # Không thấy 401/403 -> chấp nhận tạm (endpoint health có thể không tồn tại)
        return True

    @classmethod
    def validate_api_key(
        cls,
        header: str = "x-api-key",
        scheme: Optional[str] = None,
        probe_paths: Iterable[str] = ("/v1/ping", "/ping", "/healthz", "/status", "/"),
        timeout: float = 5.0,
    ) -> bool:
        """
        Giữ lại bản validate dựa trên key đã lưu (backward-compatible).
        """
        key = cls.get_api_key()  # may raise APIKeyNotSetError
        return cls._probe_api_key(key, header=header, scheme=scheme, probe_paths=probe_paths, timeout=timeout)


def client(
    apikey: str,
    *,
    verify: bool = True,  # mặc định verify NGAY khi set
    header: str = "x-api-key",
    scheme: Optional[str] = None,
    probe_paths: Iterable[str] = ("/v1/ping", "/ping", "/healthz", "/status", "/", "/list-liquid-asset"),
    timeout: float = 5.0,
):
    """
    Convenience: set (and by default verify) the API key.
    Nếu key sai -> raise InvalidAPIKeyError và KHÔNG lưu key.
    """
    Config.set_api_key(
        apikey,
        verify=verify,
        header=header,
        scheme=scheme,
        probe_paths=probe_paths,
        timeout=timeout,
    )
