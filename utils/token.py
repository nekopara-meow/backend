import time
from django.core import signing
import hashlib

HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = "Couteau"
SALT = "www.yaseal.space"


def encrypt(obj):
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def decrypt(src):
    src = signing.b64_encode((src.encode())).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    return raw


def create_token(username):
    header = encrypt(HEADER)

    payload = {"username": username, "iat": time.time(),
               "exp": time.time() + 1209600.0}
    payload = encrypt(payload)

    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    return token


def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload


def get_username(token):
    payload = get_payload(token)
    return payload['username']


def get_exp_time(token):
    payload = get_payload(token)
    return payload['exp']


def check_token(username, token):
    return get_username(token) == username and get_exp_time(token) > time.time()
