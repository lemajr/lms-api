from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import jwt, ExpiredSignatureError
from app.core.config import settings
from jwt.exceptions import InvalidTokenError
from app.schemas.user import TokenData
import pytz

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # Get the current time in UTC
    utc_time = datetime.now(timezone.utc)

    # Set the timezone to East Africa
    east_africa_timezone = pytz.timezone('Africa/Dar_es_Salaam')

    # Convert the UTC time to East Africa time
    utc_now = utc_time.astimezone(east_africa_timezone)
    print(f'Starting Time before expire: {utc_now}')


    # Calculate the expiration time based on the provided delta
    if expires_delta:
        expire = utc_now + expires_delta
    else:
        # Set token expiration to 30 minute from now
        expire = utc_now + timedelta(minutes=3)
    
    to_encode.update({"exp": expire})
    print(f"Token will expire at: {expire.strftime('%Y-%m-%d %H:%M:%S')}")
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception)->TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("Token Payload:", payload)

        username: str = payload.get("sub")
        role: str = payload.get("role")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, role=role)
        return token_data
    except ExpiredSignatureError:
        print("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please login again."
        )
    except InvalidTokenError:
        raise credentials_exception

