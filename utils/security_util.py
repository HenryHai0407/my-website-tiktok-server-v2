import jwt
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME = 3600

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityUtil:

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt algorithm

        Args:
            password (str): The plain text password to hash

        Returns:
            str: The hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash

        Args:
            plain_password (str): The plain text password to verify
            hashed_password (str): The hashed password to verify against

        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def generate_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.dict()  # Convert the Pydantic model to a dictionary
        expire = datetime.now() + \
            (expires_delta or timedelta(seconds=ACCESS_TOKEN_LIFETIME))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token
