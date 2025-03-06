import bcrypt
import jwt
from ...config import JWTAuthConfig

jwtauth = JWTAuthConfig()

def hash_password(password:str):
    return bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())

def verify_password(password:str,hashed_password:str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"),hashed_password.encode("utf-8"))


def encode_jwt(
        payload:dict,
        private_key:str = jwtauth.private_key_path.read_text(),
        algorithm:str = jwtauth.algorithm
)-> str:
    return jwt.encode(payload,private_key,algorithm=algorithm)

def decode_jwt(
        token:str,
        public_key:str = jwtauth.public_key_path.read_text(),
        algorithm:str = jwtauth.algorithm
) -> str:
    return jwt.decode(token,public_key,algorithms=[algorithm])