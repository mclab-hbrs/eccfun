from Curve25519Concise import *
import random

# Helper functions, trimming needs to be added here...
# See beginning of page 5 of https://cr.yp.to/ecdh/curve25519-20060209.pdf
# or here: https://github.com/msotoodeh/curve25519/blob/master/source/curve25519_utils.c
def encode_point(P):
    x = to_affine(P)
    return x.to_bytes(32, "little")


def decode_point(val):
    P = XZPoint(int.from_bytes(val, "little"), 1)
    return P

def trim_secret(secret):
    X = bytearray(secret.to_bytes(32, "little"))
    X[0] &= 0xf8;
    X[31] = (X[31] | 0x40) & 0x7f;
    return int.from_bytes(X, "little")


# Alice's side
# Create Secret Key
alice_secret = trim_secret(random.randint(2, 2**255-19))
# Create public key that we can send over
# untrustworthy channel
alice_public = encode_point(scalarmult(alice_secret, G))

print("Alice's public key is: ", alice_public.hex())

# Bob's side
# Create Secret Key
bob_secret = trim_secret(random.randint(2, 2**255-19))
# Create public key that we can send over
# untrustworthy channel
bob_public = encode_point(scalarmult(bob_secret, G))
print("Bob's public key is: ", bob_public.hex())

# Agree on shared secret
# Alice's side
alice_shared_secret = scalarmult(alice_secret, decode_point(bob_public))

# Bob's side
bob_shared_secret = scalarmult(bob_secret, decode_point(alice_public))

assert(to_affine(alice_shared_secret) == to_affine(bob_shared_secret))
print("Agreed upon secret is: ", encode_point(alice_shared_secret).hex())

