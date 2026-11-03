"""Rate limiting en memoria con ventana deslizante por clave (IP + ruta).

- Usa `time.monotonic()` para resistir saltos de reloj.
- GC automático cuando el dict supera `_MAX_KEYS` para evitar memory DoS
  con IPs rotativas.
"""

import threading
import time
from collections import defaultdict


_MAX_KEYS = 50_000


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        if max_requests <= 0 or window_seconds <= 0:
            raise ValueError("max_requests y window_seconds deben ser > 0")
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._buckets: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            if len(self._buckets) > _MAX_KEYS:
                self._gc(cutoff)
            bucket = [t for t in self._buckets.get(key, []) if t > cutoff]
            if len(bucket) >= self.max_requests:
                self._buckets[key] = bucket
                return False
            bucket.append(now)
            self._buckets[key] = bucket
            return True

    def _gc(self, cutoff: float) -> None:
        for k in list(self._buckets.keys()):
            fresh = [t for t in self._buckets[k] if t > cutoff]
            if fresh:
                self._buckets[k] = fresh
            else:
                del self._buckets[k]


contact_limiter = RateLimiter(max_requests=5, window_seconds=60)
login_limiter = RateLimiter(max_requests=10, window_seconds=300)