from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

API_VERSION = '0.2.0'

api = FastAPI(
    title=f"HealthID API v{API_VERSION}",
    openapi_url="/api/v1/openapi.json"
)

fake_db = {
    '99775533@healthid.life': {
        'uuid':'9e04976d-f74c-4d1d-aa2a-0f9dba7a85ad',
        'email':'99775533@healthid.life'
    }
}



if "API_ENV" in os.environ and os.environ['API_ENV'] == 'DOCKER':
    vue_dir = "./vue/"
else:
    vue_dir = "../vue/dist/"

api.mount("/ui", StaticFiles(directory=vue_dir), name="static")

@api.get('/SignIn')
def ui_signin():
    response = RedirectResponse(url='/ui/SignIn.html')
    return response

@api.get('/info')
def public_info():
    return {
        'description':'HealthID API',
        'version':f'{API_VERSION}'
    }

@api.get('/acc/{acc}/')
def get_account(acc: str):
    if not acc in fake_db:
        raise HTTPException(status_code=404, detail="Account not found")
    account = fake_db[acc]
    return account
