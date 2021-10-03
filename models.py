from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
import json
from os import urandom
import pyscrypt
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from key import generateKeyPair
 
login = LoginManager()
db = SQLAlchemy()
 
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    passkey = db.Column(db.String(500))
    publickey = db.Column(db.String(500))
    secret = db.Column(db.String(500))
 
    def createAccount(self, pwd):
        salt = urandom(16)
        key = pyscrypt.hash(pwd.encode(), salt, 2048, 8, 1, 16)
        passKey = b64encode(key).decode('utf-8')+"$"+b64encode(salt).decode('utf-8')
        privateKey, publicKey = generateKeyPair()
        cipher = AES.new(key, AES.MODE_CBC)
        secret = cipher.encrypt(pad(privateKey.encode(), AES.block_size))
        secretKey = b64encode(secret).decode('utf-8')+"$"+b64encode(cipher.iv).decode('utf-8')
        self.passkey = passKey
        self.publickey = publicKey
        self.secret = secretKey

    def loginAccount(self, pwd):
        origPass = self.passkey.split("$")
        passkey = b64decode(origPass[0])
        salt = b64decode(origPass[1])
        key = pyscrypt.hash(pwd.encode(), salt, 2048, 8, 1, 16)
        return passkey == key

class Files(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    contents = db.Column(db.Text())
    size = db.Column(db.Integer())
    lastModified = db.Column(db.DateTime)
    owner = db.Column(db.String(50))
    sharedwith = db.Column(db.String(50))
    accesskey = db.Column(db.String(500))

    def __init__(self, name, contents, size, lastmodified, owner, shareWith, accesskey):
        self.name = name
        self.contents = contents
        self.size = size
        self.lastModified = lastModified
        self.owner = owner
        self.sharedwith = sharedwith 
        self.accesskey = accesskey

@login.user_loader
def load_user(username):
    return User.query.get(username)
