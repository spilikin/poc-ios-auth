#!/usr/bin/env python3.8
from jose import jws
import sys
import os
from ecdsa import SigningKey, BRAINPOOLP256r1
import requests
import json
import base64
import argparse

CLIENT_ID='public_client'
REDIRECT_URI='http://localhost:8080/'
ENDPOINT="http://localhost:8000/api/"


parser = argparse.ArgumentParser(description='Authenticate and return the bearer token')
parser.add_argument('acct', type=str, help='Account name')
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
parser.add_argument("--endpoint", "-e", help="specify different API endpoint", default=ENDPOINT)
args = parser.parse_args()


endpoint = args.endpoint

acct=args.acct
dir=f'./accounts/{acct}'

if not os.path.exists(dir):
    print (f"Account '{acct}' not enrolled.")

# read signing key from PEM file
sk = SigningKey.from_pem(open(f'{dir}/signing_key.pem').read())

# request auth challenge from the API
challenge = requests.get(f'{endpoint}auth/challenge?acct={acct}&redirect_uri={REDIRECT_URI}').json()
if args.verbose:
    print("Got challenge from server:")
    print (json.dumps(challenge, indent=2))

# sign the nonce using JWS
signed_challenge = jws.sign({ 'nonce': challenge['nonce']}, sk.to_pem(), algorithm="ES256")
if args.verbose:
    print("Signed nonce:")
    print (signed_challenge)

# create signed challenge request JSON structure
signed_challenge_request = { 
    'signed_nonce': signed_challenge,
    'nonce': challenge['nonce'],
    'acct': challenge['acct']
}

if args.verbose:
    print("Sending signed challenge to server:")
    print (json.dumps(signed_challenge_request, indent=2))

# POST the signed enrollment request to the enrollment endpoint
resp=requests.post(
    f'{endpoint}auth/challenge',
    data=json.dumps(signed_challenge_request)
)

# we should receive the code 
if resp.status_code != 200:
    print(f"Error: {resp.status_code} {resp.text}")
    exit(1)
    
code_response = resp.json()
if args.verbose:
    print (json.dumps(code_response, indent=2))

# use the code to fetch the token
resp = requests.post(
    url=f'{endpoint}auth/token',
    data={
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": code_response['code'],
        "code_verifier": "none",
    },
    allow_redirects=False
)

# wel should receive the access_token as part of the json response
result = resp.json()
if args.verbose:
    print(json.dumps(result, indent=2))

def _b64_decode(data):
    data += '=' * (4 - len(data) % 4)
    return base64.b64decode(data).decode('utf-8')

def jwt_payload_decode(jwt):
    _, payload, _ = jwt.split('.')
    return json.loads(_b64_decode(payload))

if args.verbose:
    print("Access token content:")
    print(json.dumps(jwt_payload_decode(result['access_token']), indent=2))

if args.verbose:
    print ("And the bearer is:")

print (result['access_token'])