from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

API_VERSION = '0.4.0'

api = FastAPI(
    title=f"HealthID API v{API_VERSION}",
)

mock_db = [
    {
        'uuid':'9e04976d-f74c-4d1d-aa2a-0f9dba7a85ad',
        'subj':'99775533@healthid.life',
        'email':'99775533@healthid.life'
    }
]

@api.get('/info')
def public_info():
    return {
        'description':'HealthID API',
        'version':f'{API_VERSION}'
    }

@api.get('/acc/{subj}/')
def get_account(subj: str):
    matches = [acc for acc in mock_db if acc['subj'] == subj]
    if len(matches) == 0:
        raise HTTPException(status_code=404, detail="Account not found")

    account = matches[0]
    return account
