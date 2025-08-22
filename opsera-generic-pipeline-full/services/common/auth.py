from fastapi import Header, HTTPException

def require_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key is None or x_api_key != "demo-key":
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
