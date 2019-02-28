from .EllipticCurve import EllipticCurve
from .AffinePoint import AffinePoint


class WeierstrassCurve(EllipticCurve):

    def __init__(self, a, b, mod):
        self.a = a
        self.b = b
        self.mod = mod
        self.poif = AffinePoint(self, "infinity", "infinity")

    def is_singular(self):
        return (-16 * (4 * self.a**3 + 27 * self.b ** 2)) % self.mod == 0

    def _exp(self, base, e):
        return pow(base, e, self.mod)

    def calc_y_sq(self, x):
        return (self._exp(x, 3) + self.a * x + self.b) % self.mod

    def invert(self, point):
        return AffinePoint(self, point.x, (-1 * point.y) % self.mod)

    def is_on_curve(self, point):
        return point is self.poif or self.calc_y_sq(point.x) == self._exp(point.y, 2)

    def add(self, P, Q):
         """
         Sum of the points P and Q.
         Rules: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
         """
         if not (self.is_on_curve(P) and self.is_on_curve(Q)):
             raise ValueError("Points not on basic_curves")

         # Cases with POIF
         if P == self.poif:
             result = Q
         elif Q == self.poif:
             result = P
         elif Q == self.invert(P):
             result = self.poif
         else: # without POIF
             if P == Q:
                 slope = (3 * P.x**2 + self.a) * self.inv_val(2 * P.y)
             else:
                 slope = (Q.y - P.y) * self.inv_val(Q.x - P.x)
             x = (slope**2 - P.x - Q.x) % self.mod
             y = (slope * (P.x - x) - P.y) % self.mod
             result = AffinePoint(self, x, y)

         return result

    def __str__(self):
        return "y^2 = x^3 + {}x + {} mod {}".format(self.a, self.b, self.mod)
