from pydantic import BaseModel
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
import time

ISSUER='https://id.acme.spilikin.dev/'
TOKEN_VALIDITY_PERIOD=30*60 # 30 Minutes
PRIVATE_KEY='''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIN13TiYprZRuj+j8+B/AX7WDdv3UFc1oWqYm/YbkgPtXoAoGCCqGSM49
AwEHoUQDQgAErLyoIuOaiTLTArey9gi3VYuAA6Z6o2KktN2C1bHwK9At0pmCLxLG
MwAYWevVcsANaPgwM9KAmJ83meXmoTNuHg==
-----END EC PRIVATE KEY-----
'''
PUBLIC_KEY='''-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAErLyoIuOaiTLTArey9gi3VYuAA6Z6
o2KktN2C1bHwK9At0pmCLxLGMwAYWevVcsANaPgwM9KAmJ83meXmoTNuHg==
-----END PUBLIC KEY-----
'''

oauth2 = OAuth2AuthorizationCodeBearer(authorizationUrl='auth', tokenUrl='token')

class User(BaseModel):
    acct: str

def get_user(token: str = Depends(oauth2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, PUBLIC_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return User(acct=username)

def impersonate(acct: str):
    token_data = {
        'iss': ISSUER,
        'sub': acct,
        'exp': int(time.time())+TOKEN_VALIDITY_PERIOD
    }
    token = jwt.encode(token_data, PRIVATE_KEY, algorithm='ES256')
    return token