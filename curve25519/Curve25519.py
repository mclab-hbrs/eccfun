"""
Sources:
[1] Guide to Elliptic Curve Cryptography, Hankerson
"""
PRIME = 2**255-19
BASE_X = 9
A = 486662
ORDER = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed


def square(x):
    return pow(x, 2, PRIME)


def inv(x):
    return pow(x, PRIME-2, PRIME)


class XZPoint:

    def __init__(self, x, z=1):
        self.x = x
        self.z = z

    @property
    def affine(self):
        """
        Converts the projective/jacobian coordinates into the affine
        x value.
        """
        return self.x * inv(self.z) % PRIME

    def _double(self):
        """
        Double function used to calculate the x value of 2P.
        Since z1 is set to 1, this has to be used in the montgommery latter
        where the x value of the base point is used as x1 in the add step.
        """
        plus_sq = square(self.x + self.z)
        minus_sq = square(self.x - self.z)
        new_x = plus_sq * minus_sq % PRIME
        new_z = (plus_sq - minus_sq) * (plus_sq + ((A-2)//4) * (plus_sq - minus_sq)) % PRIME
        return XZPoint(new_x, new_z)

    def _add(self, Q, base):
        """
        Add function used to calculate P + Q.
        This uses the value x1 = x value of base point.
        This works since we use the montgommery ladder and
        r[1] is always r[0] + base point. 
        So, we know that r[1] - r[0] = BASE_POINT, so we can just set x1 = BASE_POINT
        :param Q: Point to add to this point
        :param base: This is the base point, in other words r[1] - r[0], P - Q
        :return: Jacobian point P + Q
        """
        new_x = square((self.x - self.z)*(Q.x + Q.z) + (self.x + self.z) * (Q.x-Q.z))
        new_z = square((self.x - self.z)*(Q.x + Q.z) - (self.x + self.z) * (Q.x-Q.z)) * base % PRIME
        return XZPoint(new_x, new_z)

    def copy(self):
        return XZPoint(self.x, self.z)

    def __rmul__(self, k):
        if type(k) != int:
            raise ValueError("Can't multiply point by type {}".format(type(k)))
        return self.scalarmult(k)

    def scalarmult(self, k):
        """
        This implements the scalarmultiplication kP.
        It uses the montgommery ladder to do so.
        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Montgomery_ladder
        We go through all bits of the multiplier k,
        if the current bit is 0:
            set r[0] = (2l)P
                r[1] = (2l+1)P
        if the current bit is 1:
            set r[0] = (2l+1)P
                r[1] = (2l+2)P
        where l is the integer represented by the l leftmost bits of k.
        For details see [1] (p. 102).
        """
        r = [XZPoint(1, 1), self.copy()]
        base = self.affine

        for i in range(k.bit_length(), -1, -1):
            di = (k >> i) & 0x1
            if di:
                r[0] = r[0]._add(r[1], base)
                r[1] = r[1]._double()
            else:
                r[1] = r[0]._add(r[1], base)
                r[0] = r[0]._double()

        return r[0]

    def __str__(self):
        return "XZPoint({},{})".format(self.x, self.z)


BASE_POINT = XZPoint(BASE_X)


class Curve25519:

    def __init__(self, sk):
        self.sk = sk
        self._pub_point = self.sk * BASE_POINT
        self.pk = self._pub_point.affine

    def compute_shared(self, pk):
        p = XZPoint(pk)
        return (self.sk * p).affine


G = XZPoint(BASE_X)
assert(((ORDER+1) * G).affine == BASE_X)

P = 1337 * G
Q = 1234 * G

assert P.affine != Q.affine
X = 1234 * P
Y = 1337 * Q
assert(X.affine == Y.affine)

PQ_diff = (1337 - 1234) * G
QP_diff = (1234 - 1337) * G
assert(P._add(Q, PQ_diff.affine) == Q._add(P, QP_diff.affine))
