from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
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

class EnrollmentRequest(BaseModel):
    acct: str
    email: str
    device_public_key: str

class SignedEnrollmentRequest(BaseModel):
    req: str # base64 encoded EnrollmentRequest
    sig: str

class Account(BaseModel):
    uuid: str
    acct: str
    email: str

class Challenge(BaseModel):
    nonce: str
    exp: int
    acct: str

API_VERSION = '0.5.0'

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
def get_challenge(acct: str):
    db.challenges.remove(db.where('exp') < time.time())
    challenge = { 
        'exp': int(time.time())+300,
        'acct': acct,
        'nonce': secrets.token_hex(32) 
    }
    db.challenges.insert(challenge)
    return challenge