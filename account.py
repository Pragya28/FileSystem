import json
from os import urandom
import pyscrypt
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from key import generateKeyPair

def createAccount(uname, pwd):
    salt = urandom(16)
    key = pyscrypt.hash(pwd.encode(), salt, 2048, 8, 1, 16)
    passKey = b64encode(key).decode('utf-8')+"$"+b64encode(salt).decode('utf-8')
    privateKey, publicKey = generateKeyPair()
    cipher = AES.new(key, AES.MODE_CBC)
    secret = cipher.encrypt(pad(privateKey.encode(), AES.block_size))
    secretKey = b64encode(secret).decode('utf-8')+"$"+b64encode(cipher.iv).decode('utf-8')
    return (uname, passKey, publicKey, secretKey)