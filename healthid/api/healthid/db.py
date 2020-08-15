from tinydb import TinyDB, where
from os import makedirs, environ
makedirs('.db', exist_ok=True)

if "API_ENV" in environ and environ['API_ENV'] == 'DOCKER':
    db_location = "../healthid_db/db.json"
else:
    db_location = "./.db/db.json"

db = TinyDB(db_location)

accounts = db.table('account')
challenges = db.table('challenge')
codes = db.table('codes')
auditlog = db.table('auditlog')

