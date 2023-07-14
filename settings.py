from datetime import timedelta


title = 'Read Craft Academy'
host = 'localhost'
port = 8000
origins = [
    'http://localhost:8000',
    'http://localhost',
    'http://localhost:3000'
]
secret = 'super secret'
access_token_lifetime = timedelta(days=0, minutes=15, seconds=0)
refresh_token_lifetime = timedelta(days=14, minutes=0, seconds=0)
