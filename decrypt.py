from base64 import b64decode
import hmac
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from keys import generateSymmetricKey

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

def decryptMsg(c, ke, iv):
    cipher = AES.new(ke, AES.MODE_CBC, iv)
    m = unpad(cipher.decrypt(c), AES.block_size)
    return m.decode()

def decryptFile(filepath, info, shared):
    salt, iv = getInfo(info)    
    secret = shared + filepath.split("\\")[-1]
    ke, km = generateSymmetricKey(secret, salt)
    with open(filepath, "r") as f:
        msg = f.read()
    c, mTag = getMsgInfo(msg)
    if verifyTag:
        contents = decryptMsg(c, ke, iv)
    else:
        contents = "Failed"
    return contents

# salt = b'\x89\xdd`\x8a7\x87\xf6\x97\xa6}\x8c2\xe1,\xc2\x01\x81\x8f\xd0G&\xcc\xd1r<\xa8d\xb1[\x84\x91\x9c\xc3\xc5O\xd4M\xcf8\x155\x96\x01\r\xa0\x1c,\x8b\x00\xa3\xc5\xe7\xa1\xa4\xb8\\\x8e\xbd\xab\x9b7\xc1} j\x97F\xfc\xffjY\x9b\xc77\x1c\xfb\xb4\xb1]I1DA\xa9\x9f\x7f\x90\xab\xe1\x04\xea\xfd\xb7}\x93\x04\x9c\xe3Z\x87\x05\x03\xf1\t\xe7\x1f\xb2\x83\xf9\xf7&3\x1dg\xa0\x11&O-\x98\x05p\x08\x93Q1\xeb\xf1'
# iv = b'\x98\xb3\xe9\xb9\x86_.\x12_\x96\\\x1c\xd5[\x12\xd1'
# x = "OTUwMDg3NzAwODUwOTc5OTU0MDY3NjMxMzE4MTk5MjMwODE0ODgxNDM3MTIxNzY3NTIxMTU5NjQ4ODA3MTExMjUzMzk2NTU3NTEzNzY=$NjYzMTcyOTExOTgwMDg4ODczNzQxOTk5MjEyNjg0MTg5NzA5Nzc1MTc5OTY5MjI3NzAwMTI1ODk3MTYxNDIzMjA2MDA1OTE3MTQyNTg=$id1gijeH9pemfYwy4SzCAYGP0EcmzNFyPKhksVuEkZzDxU/UTc84FTWWAQ2gHCyLAKPF56GkuFyOvaubN8F9IGqXRvz/almbxzcc+7SxXUkxREGpn3+Qq+EE6v23fZMEnONahwUD8QnnH7KD+fcmMx1noBEmTy2YBXAIk1Ex6/E=$mLPpuYZfLhJfllwc1VsS0Q=="
# salt, iv = getInfo(x)
# print(salt)
# print(iv)
# print(decryptFile(r"D:\\MSIT\\2020501042\\Cryptography\\FileSystem - 2 Users\\User A\\testfile"))