
from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime, timedelta

from app.config import settings
from app.postgres_connect import get_db
from app.model import User
from app.schemas.token import TokenData


oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        user_name: str = payload.get("user_name")

        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id, user_name=user_name)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: Annotated[str, Depends(oauth2_schema)],
                     db: Annotated[Session, Depends(get_db)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter_by(id=token.id).first()

    if user is None:
        raise credentials_exception

    return user


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    


def get_current_ceo_user(
    current_user: User = Depends(get_current_user)
):
    ceo_emails = [
        "diallo30amadoukorka@gmail.com",
        "support@groupegenetics.com",
        "mohamed.thialaw@groupegenetics.com"
    ]

    if current_user.email not in ceo_emails:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Action réservée au CEO de l'entreprise"
        )

    return current_user


