from curves import MontgommeryCurve
from curves import AffinePoint

# Curve25519 is a Montgommery Curve
# Every montgommery curves is birationally equivalent
# to a twisted edwards curve.
# Which means every montgommery curve can be converted
# to a twisted edwards curve.
# Which means Curve25519 can be converted to ed25519 and vice versa.
Curve25519 = MontgommeryCurve(123, 7, 2503)
Curve25519.plot().show()