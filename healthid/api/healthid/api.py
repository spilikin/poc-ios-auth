from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

API_VERSION = '0.9.0'
    
api = FastAPI(
    title=f"HealthID API",
    version=API_VERSION
)

from .routers import account
api.include_router(account.router)
from .routers import auth
api.include_router(auth.router)

@api.get('/info')
def public_info():
    return {
        'description':'HealthID API',
        'version':f'{API_VERSION}'
    }
