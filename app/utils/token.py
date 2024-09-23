from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import jwt, ExpiredSignatureError
from app.core.config import settings
from jwt.exceptions import InvalidTokenError
from app.schemas.user import TokenData

 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Set token expiration
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print(f"Token will expire at: {expire}")
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
local_tz = pytz.timezone('Africa/Dar_es_Salaam')
expire_time_local = expire_time_utc.astimezone(local_tz)

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        return token_data
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please login again."
        )
    except InvalidTokenError:
        raise credentials_exception
    