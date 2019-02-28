from .AffinePoint import AffinePoint
from .EllipticCurve import EllipticCurve


class EdwardsCurve(EllipticCurve):

    def __init__(self, d, mod, a=1):
        """
        General Edwards Curve.
        If a!=1, the basic_curves is twisted.
        """
        self.d = d % mod
        self.a = a
        self.mod = mod
        # By definition, so we can do the addition as below
        self.neutral_element = AffinePoint(self, 0, 1)
        # TODO: Check if d is not a square in K

    def is_on_curve(self, P):
        x_sq = pow(P.x, 2, self.mod)
        y_sq = pow(P.y, 2, self.mod)
        return (self.a * x_sq + y_sq)%self.mod == (1 + self.d * x_sq * y_sq) % self.mod

    def add(self, P, Q):
        """
        Sum of points P and Q.
        https://en.wikipedia.org/wiki/Edwards_curve#The_group_law
        """
        if not (self.is_on_curve(P) and self.is_on_curve(Q)):
            raise ValueError("Points not on basic_curves")
        den_x = 1 + (self.d * P.x * P.y * Q.x * Q.y) % self.mod
        den_y = 1 - (self.d * P.x * P.y * Q.x * Q.y) % self.mod

        nom_x = P.x * Q.y + Q.x * P.y % self.mod
        nom_y = P.y * Q.y - self.a * Q.x * P.x % self.mod

        return AffinePoint(
                self,
                nom_x * self.inv_val(den_x) % self.mod,
                nom_y * self.inv_val(den_y) % self.mod
        )

    def __str__(self):
        return "{}x^2 + y^2 = 1 + {}x^2y^2 mod {}".format(self.a, self.d, self.mod)
