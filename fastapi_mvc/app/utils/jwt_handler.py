from datetime import datetime, timedelta
from jose import JWTError, jwt

# You should use environment variables for production
SECRET_KEY = "iNkL1PA8l9Zm_-VuB02rL5HtIOuLxod8yDfcOHhKuf2L3dxGxAmVvBzZAjX7rTnrx1wwpZclc_TNWRYwZzVuDQ"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode or '', SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
