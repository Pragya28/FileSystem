from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hmac
from hashlib import sha256
from base64 import b64encode

from keys import generateSymmetricKey

def encryptMsg(m, ke, km, iv):
    cipher = AES.new(ke, AES.MODE_CBC, iv)
    c = cipher.encrypt(pad(m, AES.block_size))
    d = hmac.new(km, c+iv, sha256).digest()
    return b64encode(c).decode('utf-8')+"$"+b64encode(d).decode('utf-8')

def encryptFile(filepath, shared):
    secret = shared + filepath.split("\\")[-1]
    salt = urandom(128)
    ke, km = generateSymmetricKey(secret, salt)
    with open(filepath, "rb") as f:
        msg = f.read()
    iv = urandom(16)
    enc = encryptMsg(msg, ke, km, iv)
    with open(filepath,"w") as f:
        f.write(enc)
    return b64encode(salt).decode('utf-8')+"$"+b64encode(iv).decode('utf-8')
