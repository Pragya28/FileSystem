from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import pyscrypt
from base64 import b64decode, b64encode
from datetime import datetime
from tinyec import ec, registry
import secrets

curve = registry.get_curve('secp256r1')

pwd_A = "12345"
pwdbytes_A = pwd_A.encode()
salt_A = urandom(16)
key_A = pyscrypt.hash(pwdbytes_A, salt_A, 2048, 8, 1, 16)
passkey_A = b64encode(key_A).decode()+"$"+b64encode(salt_A).decode()
privatekey_A = secrets.randbelow(curve.field.n)
publickey_A = privatekey_A * curve.g
publickey_A = str(publickey_A.x) + "$" + str(publickey_A.y)
privatekey_A = str(privatekey_A)
cipher_A = AES.new(key_A, AES.MODE_CBC)
iv_A = cipher_A.iv
secret_A = cipher_A.encrypt(pad(privatekey_A.encode(), AES.block_size))
secretkey_A = b64encode(secret_A).decode()+"$"+b64encode(iv_A).decode()


pwd_Q = "00000"
pwdbytes_Q = pwd_Q.encode()
salt_Q = urandom(16)
key_Q = pyscrypt.hash(pwdbytes_Q, salt_Q, 2048, 8, 1, 16)
passkey_Q = b64encode(key_Q).decode()+"$"+b64encode(salt_Q).decode()
privatekey_Q = secrets.randbelow(curve.field.n)
publickey_Q = privatekey_Q * curve.g
publickey_Q = str(publickey_Q.x) + "$" + str(publickey_Q.y)
privatekey_Q = str(privatekey_Q)
cipher_Q = AES.new(key_Q, AES.MODE_CBC)
iv_Q = cipher_Q.iv
secret_Q = cipher_Q.encrypt(pad(privatekey_Q.encode(), AES.block_size))
secretkey_Q = b64encode(secret_Q).decode()+"$"+b64encode(iv_Q).decode()


key_Ad = b64decode(passkey_A.split("$")[0].encode())
s = secretkey_A.split("$")
secret_Ad = b64decode(s[0].encode())
iv_Ad = b64decode(s[1].encode())
cipher_Ad = AES.new(key_Ad, AES.MODE_CBC, iv_Ad)
privatekey_Ad = unpad(cipher_Ad.decrypt(secret_Ad), AES.block_size)
privatekey_Ad = int(privatekey_Ad.decode())
# privatekey_Ad = int.from_bytes(privatekey_Ad, byteorder='big')
publickey_Qd = publickey_Q.split("$")
x = int(publickey_Qd[0])
y = int(publickey_Qd[1])
publickey_Qd = ec.Point(curve, x, y)
shared_AQ = privatekey_Ad * publickey_Qd
secret_AQ = hex(shared_AQ.x) + hex(shared_AQ.y % 2)[2:]

key_Qd = b64decode(passkey_Q.split("$")[0].encode())
s = secretkey_Q.split("$")
secret_Qd = b64decode(s[0].encode())
iv_Qd = b64decode(s[1].encode())
cipher_Qd = AES.new(key_Qd, AES.MODE_CBC, iv_Qd)
privatekey_Qd = unpad(cipher_Qd.decrypt(secret_Qd), AES.block_size)
privatekey_Qd = int(privatekey_Qd.decode())
# privatekey_Qd = int.from_bytes(privatekey_Qd, byteorder='big')
publickey_Ad = publickey_A.split("$")
x = int(publickey_Ad[0])
y = int(publickey_Ad[1])
publickey_Ad = ec.Point(curve, x, y)
shared_QA = privatekey_Qd * publickey_Ad
secret_QA = hex(shared_QA.x) + hex(shared_QA.y % 2)[2:]

print(shared_AQ == shared_QA)
