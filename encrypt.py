from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hmac
from hashlib import sha256
from base64 import b64encode

from keyGenerators import generateSymmetricKey

def encrypt(filename, shared, content):
    secret = shared + filename
    salt = urandom(128)
    ke, km = generateSymmetricKey(secret, salt)
    iv = urandom(16)
    cipher = AES.new(ke, AES.MODE_CBC, iv)
    c = cipher.encrypt(pad(content, AES.block_size))
    d = hmac.new(km, c+iv, sha256).digest()
    enc = b64encode(c).decode('utf-8')+"$"+b64encode(d).decode('utf-8')
    ka = b64encode(salt).decode('utf-8')+"$"+b64encode(iv).decode('utf-8')
    return enc, ka