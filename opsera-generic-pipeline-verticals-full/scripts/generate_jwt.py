#!/usr/bin/env python3
import argparse, time, json, base64, hmac, hashlib

def b64url(b: bytes) -> str:
  return base64.urlsafe_b64encode(b).decode().rstrip("=")

ap = argparse.ArgumentParser()
ap.add_argument("--secret", required=True)
ap.add_argument("--sub", required=True)
ap.add_argument("--scopes", default="")
ap.add_argument("--ttl", type=int, default=3600)
args = ap.parse_args()

header = {"alg":"HS256","typ":"JWT"}
payload = {"sub": args.sub, "scope": args.scopes, "iat": int(time.time()), "exp": int(time.time()) + args.ttl}
h_b64 = b64url(json.dumps(header, separators=(",", ":")).encode())
p_b64 = b64url(json.dumps(payload, separators=(",", ":")).encode())
signing_input = f"{h_b64}.{p_b64}".encode()
sig = hmac.new(args.secret.encode(), signing_input, hashlib.sha256).digest()
print(f"{h_b64}.{p_b64}.{b64url(sig)}")
