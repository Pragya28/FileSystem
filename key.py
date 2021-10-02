from tinyec import registry
import secrets

def generateKeyPair():
    curve = registry.get_curve('secp256r1')
    private_key = secrets.randbelow(curve.field.n)
    public_key = private_key * curve.g
    public_key = str(public_key.x) + "$" + str(public_key.y)
    return (str(private_key), public_key)