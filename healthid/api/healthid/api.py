from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import secrets
import time
import healthid.db as db
import healthid.security as security
from pydantic import BaseModel
from uuid import uuid4
import urllib.parse
from enum import Enum
import base64
import urllib

API_VERSION = '0.8.0'

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:8080",
    "https://acme.spilikin.dev",
    "https://appauth.acme.spilikin.dev",
    "https://id.acme.spilikin.dev",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class EnrollmentRequest(BaseModel):
    acct: str
    email: str
    device_public_key: str

class SignedEnrollmentRequest(BaseModel):
    enrollmentData: str # base64 encoded EnrollmentRequest
    signature: str

class Account(BaseModel):
    uuid: str
    acct: str
    email: str

class Challenge(BaseModel):
    nonce: str
    exp: int
    acct: str
    redirect_uri: str

class SignatureAlgorithm(str, Enum):
    Unsigned = 'Unsigned'
    E2S56 = 'ES256'

class SignedChallenge(BaseModel):
    acct: str
    nonce: str
    alg: SignatureAlgorithm
    signature: str

class AuthenticationCode(BaseModel):
    code: str
    exp: int
    acct: str
    redirect_uri: str



class TokenResponse(BaseModel):
    access_token: str
    


api = FastAPI(
    title=f"HealthID API",
    version=API_VERSION
)

@api.get('/info')
def public_info():
    return {
        'description':'HealthID API',
        'version':f'{API_VERSION}'
    }

@api.get('/acct/{acct}')
def get_account(acct: str, user: security.User = Depends(security.get_user)):
    matches = db.accounts.search(db.where('acct') == acct)
    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Account not found")

    account = matches[0]
    return account

@api.post('/enroll')
def enroll(req: EnrollmentRequest):
    if len(db.accounts.search(db.where('acct') == req.acct)) > 0:
        raise HTTPException(status_code=409, detail="Account already exists")
        
    account = Account(
        uuid = str(uuid4()),
        acct = req.acct,
        email = req.email)
    db.accounts.insert(account.dict())
    return account

@api.get('/auth/challenge')
def get_challenge(acct: str, redirect_uri: str, remote_auth_uri : Optional[str] = None):
    challenge = Challenge(
        exp = int(time.time())+1800, # 30 Minutes
        acct = acct,
        nonce = secrets.token_hex(32),
        redirect_uri = redirect_uri
    )
    db.challenges.insert(challenge.dict())
    if remote_auth_uri:
        url = remote_auth_uri
        url += "?acct="+acct
        url += "&nonce="+challenge.nonce
        url += "&redirect_uri="+redirect_uri
        return RedirectResponse(url)
    else:
        return challenge

@api.post('/auth/challenge')
def post_signed_challenge(signed_challenge: SignedChallenge):
    db.challenges.remove(db.where('exp') < time.time())
    # TODO: verify signature
    matches = db.challenges.search(db.where('nonce') == signed_challenge.nonce)
    if len(matches) == 0:
        raise HTTPException(status_code=400, detail="Unknown challenge")

    challenge = Challenge(**matches[0])

    code = AuthenticationCode(
        code=os.urandom(40).hex(),
        exp=int(time.time())+1800,
        acct=challenge.acct,
        redirect_uri=challenge.redirect_uri
    )
    db.codes.insert(code.dict())
    return code

@api.post('/auth/token')
def provide_token(grant_type=Form(...), code=Form(...), redirect_uri=Form(...), client_id=Form(...)):
    db.codes.remove(db.where('exp') < time.time())
    # grant_type REQUIRED.  Value MUST be set to "authorization_code".
    matches = db.codes.search(db.where('code') == code)
    if len(matches) == 0:
        raise HTTPException(status_code=400, detail="Unknown code")

    auth_code = AuthenticationCode(**matches[0])
    parts = urllib.parse.urlparse(auth_code.redirect_uri)
    audience = result = f'{parts.scheme}://{parts.netloc}/'
    access_token = security.issue_token(acct = auth_code.acct, audience = audience)

    return TokenResponse(
        access_token = access_token
    )