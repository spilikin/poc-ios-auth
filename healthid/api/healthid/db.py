from tinydb import TinyDB, where
from os import makedirs
makedirs('.db', exist_ok=True)
db = TinyDB('.db/db.json')

accounts = db.table('account')
challenges = db.table('challenge')

challenges.truncate()

def create_testdata():
    accounts.insert(
    {
        'uuid':'9e04976d-f74c-4d1d-aa2a-0f9dba7a85ad',
        'acct':'99775533@healthid.life',
        'email':'99775533@healthid.life'
    })

if len(accounts) == 0:
    create_testdata()


