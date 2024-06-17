import secrets
import hashlib

salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"


def generate_token():
    return hashlib.sha256(secrets.token_bytes(32)).hexdigest()


def generate_redirect_url():
    token = secrets.token_urlsafe(64)
    redirect_url = f"https://mercury-uat.phonepe.com/transact?token={token}"
    return redirect_url


def generate_checksum(payload: dict, salt_key: str) -> str:
    payload_str = (
        "".join(str(value) for value in payload.values() if value is not None)
        + salt_key
    )
    return hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

def verify_checksum(payload: dict, checksum: str, salt_key: str) -> bool:
    payload_str = (
        "".join(str(value) for value in payload.values() if value is not None)
        + salt_key
    )
    calculated_checksum = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
    return calculated_checksum == checksum



