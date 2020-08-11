from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from healthid.api import api

app = FastAPI(
    title=f"HealthID standalone WebApp",
)

app.mount('/api', api)

if "API_ENV" in os.environ and os.environ['API_ENV'] == 'DOCKER':
    vue_dir = "./vue/"
else:
    vue_dir = "../vue/dist/"

templates = Jinja2Templates(directory=vue_dir)

@app.get('/SignIn/')
def signin(request: Request):
    return templates.TemplateResponse("SignIn.html", {"request": request})

@app.get('/SignIn/{subpage}')
def signin_subpage(request: Request, subpage: str):
    return templates.TemplateResponse("SignIn.html", {"request": request})

@app.get('/Account/{account_id}/')
def account(request: Request, account_id: str):
    return templates.TemplateResponse("Account.html", {"request": request})

@app.get('/Account/{account_id}/{subpath}')
def account_subpath(request: Request, account_id: str):
    return templates.TemplateResponse("Account.html", {"request": request})


app.mount("/", StaticFiles(directory=vue_dir), name="static")
