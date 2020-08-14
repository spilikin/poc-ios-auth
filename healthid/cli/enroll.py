#!/usr/bin/env python3.8
from jose import jws
import sys
import os
from ecdsa import SigningKey, BRAINPOOLP256r1
import requests
import json
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
os.makedirs(dir, exist_ok=True)

# generate new ECC keypair
sk = SigningKey.generate(curve=BRAINPOOLP256r1)

# write private and verifying keys to files
open(f'{dir}/signing_key.pem', 'w+b').write(sk.to_pem())
open(f'{dir}/verifying_key.pem', 'w+b').write(sk.verifying_key.to_pem())

# create enrollment request JSON structure
enrollment_request = {
    'acct': acct,
    'email': acct
}

# sign the enrollment request using own private key
signed_enrollment=jws.sign(enrollment_request, sk.to_pem(), algorithm="ES256")

# create signed enrollment request JSON structure
signed_enrollment_request = { 
    'signed_enrollment': signed_enrollment,
    'verifying_key': sk.verifying_key.to_pem().decode('utf-8')
}

# POST the signed enrollment request to the enrollment endpoint
resp=requests.post(
    f'{endpoint}enroll',
    data=json.dumps(signed_enrollment_request)
)

if resp.status_code != 200:
    print(resp.text)
    exit(1)

print(json.dumps(resp.json(), indent=2, sort_keys=True))

print(f"Local account data is stored in {dir}")