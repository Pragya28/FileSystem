from base64 import b64decode
import hmac
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from keyGenerators import generateSymmetricKey

def getInfo(token):
    token = token.split("$")
    salt = b64decode(token[0])
    iv = b64decode(token[1])
    return salt, iv

def getMsgInfo(token):
    token = token.split("$")
    c = b64decode(token[0])
    d = b64decode(token[1])
    return c, d

def verifyTag(c, tag, km, iv):
    d = hmac.new(km, c+iv, sha256).digest()
    return d == tag

def decrypt(filename, info, shared, content):
    salt, iv = getInfo(info)    
    secret = shared + filename
    ke, km = generateSymmetricKey(secret, salt)
    c, mTag = getMsgInfo(content)
    if verifyTag(c, mTag, km, iv):
        cipher = AES.new(ke, AES.MODE_CBC, iv)
        m = unpad(cipher.decrypt(c), AES.block_size)
        return m.decode()
    return "Failed"
