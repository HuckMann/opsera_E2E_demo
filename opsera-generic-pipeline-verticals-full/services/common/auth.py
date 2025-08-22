import os
from typing import List, Optional
from fastapi import Header, HTTPException
import time, base64, json, hmac, hashlib

AUTH_MODE = os.getenv("AUTH_MODE", "apikey")
API_KEY = os.getenv("DEMO_API_KEY", "demo-key")
JWT_SECRET = os.getenv("DEMO_JWT_SECRET", "demo-secret")
JWT_ALGO = os.getenv("DEMO_JWT_ALGO", "HS256")

def _b64url_decode(inp: str) -> bytes:
    rem = len(inp) % 4
    if rem:
        inp += "=" * (4 - rem)
    return base64.urlsafe_b64decode(inp.encode())

def _verify_hs256(token: str, secret: str) -> dict:
    header_b64, payload_b64, sig_b64 = token.split(".")
    signing_input = f"{header_b64}.{payload_b64}".encode()
    sig = _b64url_decode(sig_b64)
    expected = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(sig, expected):
        raise ValueError("Invalid signature")
    payload = json.loads(_b64url_decode(payload_b64))
    if "exp" in payload and time.time() > payload["exp"]:
        raise ValueError("Token expired")
    return payload

def require_auth(scopes: Optional[List[str]] = None, x_api_key: Optional[str] = Header(default=None), authorization: Optional[str] = Header(default=None)):
    if AUTH_MODE == "apikey":
        if x_api_key is None or x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Missing or invalid API key")
        return {"sub": "apikey-user", "scope": "*"}
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    payload = _verify_hs256(token, JWT_SECRET)
    token_scopes = payload.get("scope", "").split()
    if scopes:
        for s in scopes:
            if s not in token_scopes and "*" not in token_scopes:
                raise HTTPException(status_code=403, detail=f"Missing scope: {s}")
    return payload
