from jose import jwt 
PRIVATE_KEY='''-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIN13TiYprZRuj+j8+B/AX7WDdv3UFc1oWqYm/YbkgPtXoAoGCCqGSM49
AwEHoUQDQgAErLyoIuOaiTLTArey9gi3VYuAA6Z6o2KktN2C1bHwK9At0pmCLxLG
MwAYWevVcsANaPgwM9KAmJ83meXmoTNuHg==
-----END EC PRIVATE KEY-----
'''
PUBLIC_KEY='''-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAErLyoIuOaiTLTArey9gi3VYuAA6Z6
o2KktN2C1bHwK9At0pmCLxLGMwAYWevVcsANaPgwM9KAmJ83meXmoTNuHg==
-----END PUBLIC KEY-----
'''
token = jwt.encode({'key': 'value'}, PRIVATE_KEY, algorithm='ES256')
print (token)
claims = jwt.decode(token, PUBLIC_KEY)
print (claims)