from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
import json
from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import pyscrypt
from base64 import b64decode, b64encode
from datetime import datetime

from keyGenerators import generateKeyPair
from encrypt import encrypt
from decrypt import decrypt

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
        passKey = b64encode(key).decode()+"$"+b64encode(salt).decode()
        privateKey, publicKey = generateKeyPair()
        cipher = AES.new(key, AES.MODE_CBC)
        secret = cipher.encrypt(pad(privateKey.encode(), AES.block_size))
        secretKey = b64encode(secret).decode()+"$"+b64encode(cipher.iv).decode()

        self.passkey = passKey
        self.publickey = publicKey
        self.secret = secretKey

    def loginAccount(self, pwd):
        origPass = self.passkey.split("$")
        passkey = b64decode(origPass[0])
        salt = b64decode(origPass[1])
        key = pyscrypt.hash(pwd.encode(), salt, 2048, 8, 1, 16)
        return passkey == key

class File(db.Model):
    __tablename__ = 'files'

    name = db.Column(db.String(50), primary_key=True)
    contents = db.Column(db.Text())
    size = db.Column(db.Integer())
    lastModified = db.Column(db.DateTime)
    owner = db.Column(db.String(50))
    sharedwith = db.Column(db.String(50))
    accesskey = db.Column(db.String(500))

    def create(self, contents, shared):
        contents = contents.encode('utf-8')
        info = encrypt(self.name, shared, contents)
        self.size = len(contents)
        self.lastModified = datetime.now().strftime("%c")
        self.contents = info[0]
        self.accesskey = info[1]

    def view(self, shared):
        return decrypt(self.name, self.accesskey, shared, self.contents)

@login.user_loader
def load_user(username):
    return User.query.get(username)
