import hashlib
import hmac
import time

import stripe


def construct_stripe_event(raw_body: bytes, signature: str, secret: str):
    return stripe.Webhook.construct_event(raw_body, signature, secret)


def verify_github_signature(raw_body: bytes, signature: str, secret: str) -> bool:
    if not signature or not signature.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def verify_slack_signature(raw_body: bytes, timestamp: str, signature: str, secret: str, max_age_seconds: int = 300) -> bool:
    if not timestamp or not signature:
        return False
    try:
        request_time = int(timestamp)
    except ValueError:
        return False
    if abs(int(time.time()) - request_time) > max_age_seconds:
        return False
    base = b"v0:" + timestamp.encode("utf-8") + b":" + raw_body
    expected = "v0=" + hmac.new(secret.encode("utf-8"), base, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def verify_statushub_token(token: str, expected_token: str) -> bool:
    return bool(token and expected_token and hmac.compare_digest(token, expected_token))
