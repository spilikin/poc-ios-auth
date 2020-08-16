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


parser = argparse.ArgumentParser(description='Performs remote authentication')
parser.add_argument('acct', type=str, help='Account name')
parser.add_argument('nonce', type=str, help='Challenge nonce')
parser.add_argument("--verbose", "-v", help="increase output verbosity", action="store_true")
parser.add_argument("--endpoint", "-e", help="specify different API endpoint", default=ENDPOINT)
args = parser.parse_args()


endpoint = args.endpoint
acct = args.acct
nonce = args.nonce

dir=f'./accounts/{acct}'

if not os.path.exists(dir):
    print (f"Account '{acct}' not enrolled.")

# read signing key from PEM file
sk = SigningKey.from_pem(open(f'{dir}/signing_key.pem').read())


# sign the nonce using JWS
signed_challenge = jws.sign({ 'nonce': nonce}, sk.to_pem(), algorithm="ES256")
if args.verbose:
    print("Signed nonce:")
    print (signed_challenge)

# create signed challenge request JSON structure
signed_challenge_request = { 
    'signed_nonce': signed_challenge,
    'nonce': nonce,
    'acct': acct
}

if args.verbose:
    print("Sending signed challenge to server:")
    print (json.dumps(signed_challenge_request, indent=2))

# POST the signed enrollment request to the enrollment endpoint
resp=requests.post(
    f'{endpoint}auth/remote',
    data=json.dumps(signed_challenge_request)
)

# we should receive the code 
if resp.status_code != 200:
    print(f"Error: {resp.status_code} {resp.text}")
    exit(1)
    
response = resp.json()
if args.verbose:
    print (json.dumps(response, indent=2))
