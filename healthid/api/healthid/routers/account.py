from fastapi import APIRouter, HTTPException, Depends
import healthid.db as db
from pydantic import BaseModel
from healthid.security import User, get_remote_user
from jose import jws
import json
from uuid import uuid4
from typing import Optional, List

router = APIRouter()

class Device(BaseModel):
    alias: Optional[str]
    verifying_key: str

class Account(BaseModel):
    uuid: str
    acct: str
    email: str
    devices: List[Device]

class EnrollmentRequest(BaseModel):
    acct: str
    email: str

class SignedEnrollmentRequest(BaseModel):
    signed_enrollment: str # JWS signed EnrollmentRequest
    verifying_key: str # ECC verifying key in PEM format

def load_account(acct: str, remote_user: User):
    if acct == remote_user.acct:
        raise HTTPException(status_code=403, detail="Access denied")

    matches = db.accounts.search(db.where('acct') == acct)
    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    account = matches[0]
    return account


@router.get('/acct/{acct}')
def get_account(acct: str, remote_user: User = Depends(get_remote_user)):
    account = load_account(acct, remote_user)
    return account

#  TODO
@router.put("/acct/{acct}/{device_slot}")
def put_device(acct: str, device_slot: int, remote_user: User = Depends(get_remote_user)):
    account = load_account(acct, remote_user)
    return None

@router.post('/enroll', response_model=Account)
def enroll(req: SignedEnrollmentRequest):
    try:
        payload = jws.verify(req.signed_enrollment, req.verifying_key, algorithms="ES256")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Unable to verify JWS: "+str(e))

    enrollment_request = EnrollmentRequest(**json.loads(payload.decode('utf-8')))

    if len(db.accounts.search(db.where('acct') == enrollment_request.acct)) > 0:
        # TODO: WARNING: Just fo the sake of flawless test usage 
        # everyone can override existing accounts!!!
        db.accounts.remove(db.where('acct') == enrollment_request.acct)
        #raise HTTPException(status_code=409, detail="Account already exists")
        
    account = Account(
        uuid = str(uuid4()),
        acct = enrollment_request.acct,
        email = enrollment_request.email,
        devices = [])
    device0 = Device(verifying_key=req.verifying_key, alias="Enrollmenr device")
    account.devices.append(device0)
    db.accounts.insert(account.dict())
    return account
