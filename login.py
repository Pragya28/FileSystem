from pwinput import pwinput
# from github import Github
from os import urandom
import pyscrypt
from base64 import b64decode, b64encode
from hashlib import sha256
import hmac
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json

from keys import generateKeyPair

def createAccount():
    uname = input("Enter your username: ")
    pwd = pwinput("Enter your password: ", mask="*")
    # token = pwinput("Enter your GitHub Personal Access Token: ", mask="*")
    # try:
    #     g = Github(token)
    #     km = urandom(16)
    #     gitLogin = hmac.new(km, g.get_user().login.encode(), sha256).digest()        
    # except:
    #     return False, None
    salt = urandom(16)
    key = pyscrypt.hash(pwd.encode(), salt, 2048, 8, 1, 16)
    passKey = b64encode(key).decode('utf-8')+"$"+b64encode(salt).decode('utf-8')
    # verificationKey = b64encode(gitLogin).decode('utf-8')+"$"+b64encode(km).decode('utf-8')
    privateKey, publicKey = generateKeyPair()
    cipher = AES.new(key, AES.MODE_CBC)
    secret = cipher.encrypt(pad(privateKey.encode(), AES.block_size))
    secretKey = b64encode(secret).decode('utf-8')+"$"+b64encode(cipher.iv).decode('utf-8')
    userData = {
        'username' : uname,
        # 'password' : pwd,
        'publickey' : publicKey,
        'passkey' : passKey,
        # 'gitVerification' : verificationKey,
        'secret' : secretKey,
        'access' : True
    }
    with open('users.json', 'r') as f:
        data = json.load(f)
    data.append(userData)
    jsonObj = json.dumps(data, indent=4)
    with open('users.json','w') as f:
        f.write(jsonObj)
    return True, userData

def loginAccount(data, pwd):
    origPass = data['passkey'].split("$")
    passkey = b64decode(origPass[0])
    salt = b64decode(origPass[1])
    key = pyscrypt.hash(pwd.encode(), salt, 2048, 8, 1, 16)
    if passkey != key:
        return False, None
    return True, data