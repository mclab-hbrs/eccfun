from curves import MontgommeryCurve
from curves import AffinePoint

# Curve25519 is a Montgommery Curve
# Every montgommery curves is birationally equivalent
# to a twisted edwards curve.
# Which means every montgommery curve can be converted
# to a twisted edwards curve.
# Which means Curve25519 can be converted to ed25519 and vice versa.
Curve25519 = MontgommeryCurve(486662, 1, 2**255-19)

# Generator
G = AffinePoint(
    Curve25519,
    # x coordinate
    9,
    # y coordinate, note that in the actual ECDH setting, we don't need the y coordinate
    # which is a feature of montgommery curves
    14781619447589544791020593568409986887264606134616475288964881837755586237401,
    # order
    0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
)

assert(Curve25519.is_on_curve(G))
assert((G.order+1) * G == G)
