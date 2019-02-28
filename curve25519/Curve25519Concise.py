"""
Sources:
[1] Guide to Elliptic Curve Cryptography, Hankerson
"""
from collections import namedtuple

XZPoint = namedtuple("Point", ("x", "z"))

PRIME = 2**255-19
BASE_X = 9
A = 486662
ORDER = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
MASK = (1 << 255) - 1


def square(x):
    return pow(x, 2, PRIME)


def inv(x):
    return pow(x, PRIME-2, PRIME)


def double_add(P, Q, base_x):
    """
    Only for multiple of G so far, change BASE for others
    """
    A = P.x - P.z % PRIME
    B = P.x + P.z % PRIME
    C = Q.x - Q.z % PRIME
    D = Q.x + Q.z % PRIME

    E = A * D % PRIME
    F = B * C % PRIME

    G = square(D)
    H = square(C)

    # Add
    new_x = square(E + F) % PRIME
    new_z = square(E - F) * base_x % PRIME

    add_res = XZPoint(new_x, new_z)

    # Double
    new_x = G * H % PRIME
    new_z = G - H % PRIME
    new_z *= G + 121665 * (G - H) % PRIME

    double_res = XZPoint(new_x, new_z)

    return add_res, double_res


def to_affine(point):
    return point.x * inv(point.z) % PRIME


def scalarmult(k, G):
    r = [XZPoint(1, 1), G]
    base_x = to_affine(G)

    for i in range(k.bit_length(), -1, -1):
        di = (k >> i) & 0x1
        oi = (di+1) % 2
        r[oi], r[di] = double_add(r[oi], r[di], base_x)

    return r[0]



BASE_POINT = XZPoint(BASE_X, 1)

G = BASE_POINT
assert(to_affine(scalarmult(ORDER+1, G)) == BASE_X)

P = scalarmult(1337, G)
Q = scalarmult(1234, G)

assert to_affine(P) != to_affine(Q)
X = scalarmult(1234, P)
Y = scalarmult(1337, Q)
assert(to_affine(X) == to_affine(Y))
