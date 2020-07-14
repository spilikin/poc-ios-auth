from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

fake_db = {
    '99775533@healthid.life': {
        'uuid':'9e04976d-f74c-4d1d-aa2a-0f9dba7a85ad',
        'email':'99775533@healthid.life'
    }
}

@app.get('/info')
def public_info():
    return {
        'description':'HealthID API',
        'version':'1.0'
    }

@app.get('/acc/{acc}/')
def get_account(acc: str):
    account = fake_db[acc]
    unless
    raise HTTPException(status_code=404, detail="Account not found")