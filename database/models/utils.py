import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_uuid() -> str:
    return str(uuid.uuid4())


def make_hash(password: str) -> str:
    return pwd_context.hash(password)


def hash_verify(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)