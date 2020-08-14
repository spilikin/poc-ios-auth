from fastapi import APIRouter, HTTPException, Depends, Form
import healthid.db as db
from pydantic import BaseModel
from healthid.security import User, get_remote_user, issue_token
from jose import jws
import json
from uuid import uuid4
from typing import Optional, List
import time
import secrets
import os
from .account import Account
from enum import Enum
import base64
import urllib


router = APIRouter()

class Challenge(BaseModel):
    nonce: str
    exp: int
    acct: str
    redirect_uri: str

class SignedChallenge(BaseModel):
    nonce: str
    # JWS signed { 'nonce': '<nonce>' }
    signed_nonce: str
    acct: str

class AuthenticationCode(BaseModel):
    code: str
    exp: int
    acct: str
    redirect_uri: str

class TokenResponse(BaseModel):
    access_token: str

@router.get('/auth/challenge')
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

@router.post('/auth/challenge')
def post_signed_challenge(signed_challenge: SignedChallenge):
    db.challenges.remove(db.where('exp') < time.time())

    # see if challenge with the nonce is still in the database
    matches = db.challenges.search(db.where('nonce') == signed_challenge.nonce)
    if len(matches) == 0:
        raise HTTPException(status_code=400, detail="Unknown challenge")
    challenge = Challenge(**matches[0])

    # check the signature
    matches = db.accounts.search(db.where('acct') == challenge.acct)
    account = Account(**matches[0])  
    try:
        signed_nonce = json.loads(jws.verify(signed_challenge.signed_nonce, 
            account.devices[0].verifying_key, 
            algorithms="ES256").decode("utf-8") )
    except:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if signed_nonce['nonce'] != challenge.nonce:
        raise HTTPException(status_code=400, detail="Bad challenge")


    code = AuthenticationCode(
        code=os.urandom(40).hex(),
        exp=int(time.time())+1800,
        acct=challenge.acct,
        redirect_uri=challenge.redirect_uri
    )
    db.codes.insert(code.dict())
    return code

@router.post('/auth/token')
def provide_token(grant_type=Form(...), code=Form(...), redirect_uri=Form(...), client_id=Form(...)):
    db.codes.remove(db.where('exp') < time.time())
    # grant_type REQUIRED.  Value MUST be set to "authorization_code".
    matches = db.codes.search(db.where('code') == code)
    if len(matches) == 0:
        raise HTTPException(status_code=400, detail="Unknown code")

    auth_code = AuthenticationCode(**matches[0])
    parts = urllib.parse.urlparse(auth_code.redirect_uri)
    audience = result = f'{parts.scheme}://{parts.netloc}/'
    access_token = issue_token(acct = auth_code.acct, audience = audience)

    return TokenResponse(
        access_token = access_token
    )