import hmac
import hashlib
import time
from ..config import settings


def sign_token(payload: str, ttl: int | None = None) -> str:
    ts = int(time.time())
    exp = ts + (ttl or settings.TOKEN_TTL_SECONDS)
    data = f"{payload}|{exp}"
    sig = hmac.new(settings.HMAC_SECRET.encode(), data.encode(), hashlib.sha256).hexdigest()
    return f"{data}|{sig}"


def verify_token(token: str) -> bool:
    try:
        parts = token.split('|')
        payload = parts[0]
        exp = int(parts[1])
        sig = parts[2]
        if int(time.time()) > exp:
            return False
        data = f"{payload}|{exp}"
        expected = hmac.new(settings.HMAC_SECRET.encode(), data.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, sig)
    except Exception:
        return False
