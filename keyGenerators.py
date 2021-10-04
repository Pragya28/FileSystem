from tinyec import ec, registry
import secrets
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import pyscrypt

def generateKeyPair():
    curve = registry.get_curve('secp256r1')
    private_key = secrets.randbelow(curve.field.n)
    public_key = private_key * curve.g
    public_key = str(public_key.x) + "$" + str(public_key.y)
    return (str(private_key), public_key)

def getMyPrivateKey(passkey, secretkey):
    key = b64decode(passkey.split("$")[0])
    s = secretkey.split("$")
    secret = b64decode(s[0])
    iv = b64decode(s[1])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    privatekey = unpad(cipher.decrypt(secret), AES.block_size)
    return privatekey

def getSharedKey(publicKey, privateKey):
    privateKey = int.from_bytes(privateKey, byteorder='big')
    publicKey = publicKey.split("$")
    x = int(publicKey[0])
    y = int(publicKey[1])
    publicKey = ec.Point(registry.get_curve("secp256r1"), x, y)
    shared = privateKey * publicKey
    secret = hex(shared.x) + hex(shared.y % 2)[2:]
    return secret

def generateSymmetricKey(secret, salt):
    key = pyscrypt.hash(secret.encode(), salt, 2048, 8, 1, 64)
    return (key[:32],key[32:])
