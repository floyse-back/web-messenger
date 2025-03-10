from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class JWTAuthConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str  = "RS256"
    access_token_expire_minutes: int = 3
    refresh_token_expire_minutes: int = 30