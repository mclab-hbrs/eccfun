from P256 import curveP256, G, p
from hashlib import sha256
from random import randint

len_mask = 2**(G.order.bit_length()+1)-1

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def inv(a):
    a %= G.order
    g, x, y = egcd(a, G.order)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % G.order

# Simple version of ECDSA, without side checks
# https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm

def create_sig(secret_key, msg, nonce):
    e = int.from_bytes(sha256(msg).digest(), "big")
    z = e & len_mask
    k = nonce
    P = k * G
    r = P.x 
    s = inv(k)  * (z  + r * secret_key) % G.order
    return r, s


def check_sig(pub_key, msg, sig):
    r, s = sig
    e = int.from_bytes(sha256(msg).digest(), "big")
    z = e & len_mask
    w = inv(s)
    u1 = z * w % G.order
    u2 = r * w % G.order
    P = u1 * G + u2 *pub_key
    return r == P.x


MSG = b"Was geht ab?"

sec_key = randint(1, G.order - 1)
pub_key = sec_key * G
print("Secret key: ", sec_key)
print("Public key: ", pub_key)

sig = create_sig(sec_key, MSG, randint(1, G.order-1))
print("Signature: ", sig)

print("Signature is valid: ", check_sig(pub_key, MSG, sig))


# Exploit nonce reuse
# Nonce reuse in ecDSA = leak of private key
MSG1 = b"Why would you reuse a nonce?"
MSG2 = b"Why not? YOLO!"

# Same nonce used...
r1, s1 = create_sig(sec_key, MSG1, 1234123412341234)
r2, s2 = create_sig(sec_key, MSG2, 1234123412341234)

z1 = int.from_bytes(sha256(MSG1).digest(), "big") & len_mask
z2 = int.from_bytes(sha256(MSG2).digest(), "big") & len_mask

# Calculate k
k = (z1 - z2) * inv((s1 - s2)) % G.order

# Once k is known, we can recover the private key
rec_priv = (s1 * k - z1) * inv(r1) % G.order

print("Recovered private key: ", rec_priv)
print("Recovered private key is correct: ", rec_priv == sec_key)

