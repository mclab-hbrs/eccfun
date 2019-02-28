from .EllipticCurve import EllipticCurve
from .AffinePoint import AffinePoint


class MontgommeryCurve(EllipticCurve):

    def __init__(self, A, B, mod):
        """
        Montgommery Curve, equivalent to twisted edwards basic_curves.
        """
        self.A = A
        self.B = B
        self.mod = mod
        self.poif = AffinePoint(self, "infinity", "infinity")
        if B * (A ** 2 - 4) == 0:
            raise ValueError("Parameters do not form a montgommery basic_curves")

    def is_on_curve(self, P):
        return self.B * P.y ** 2 % self.mod == (P.x ** 3 + self.A * P.x ** 2 + P.x) % self.mod

    def invert(self, P):
        return AffinePoint(self, P.x, -P.y)

    def add(self, P, Q):
        if not (self.is_on_curve(P) and self.is_on_curve(Q)):
            raise ValueError("Points not on basic_curves")

        if P is self.poif:
            x_new = Q.x
            y_new = Q.y
        elif Q is self.poif:
            x_new = P.x
            y_new = P.y
        elif Q == self.invert(P):
            return self.poif
        elif P == Q:
            x_new = (3 * P.x ** 2 + 2 * P.x * self.A + 1) ** 2
            x_new *= self.inv_val(4 * P.y ** 2 * self.B)
            x_new -= 2 * P.x + self.A
            y_new = (3 * P.x ** 2 + 2 * P.x * self.A + 1) * (3 * P.x + self.A) * self.inv_val(2 * P.y * self.B)
            y_new -= (3 * P.x ** 2 + 2 * P.x * self.A + 1) ** 3 * self.inv_val(8 * P.y ** 3 * self.B ** 2)
            y_new -= P.y
        else:  # P!=Q
            nom_x = self.B * (Q.x * P.y - P.x * Q.y) ** 2
            den_x = P.x * Q.x * (Q.x - P.x) ** 2

            nom_y = (2 * P.x + Q.x + self.A) * (Q.y - P.y)
            den_y = Q.x - P.x

            nom_y_1 = self.B * (Q.y - P.y) ** 3
            den_y_1 = (Q.x - P.x) ** 3

            x_new = nom_x * self.inv_val(den_x)
            y_new = nom_y * self.inv_val(den_y) - nom_y_1 * self.inv_val(den_y_1)
            y_new -= P.y

        return AffinePoint(self, x_new % self.mod, y_new % self.mod)

    def __str__(self):
        return "{}y^2 = x^3 + {}x^2 + x mod {}".format(self.B, self.A, self.mod)