from pydantic import BaseModel
from dotenv import load_dotenv
from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

class JWTAuthConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str  = "RS256"
    access_token_expire_minutes: int = 3
    refresh_token_expire_minutes: int = 30


SQLALCHEMY_DATABASE_URL = getenv("SQLALCHEMY_DATABASE_URL")