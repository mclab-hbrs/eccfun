from curves import WeierstrassCurve
from curves import AffinePoint

# Take the standardized curve, as here:
# https://tools.ietf.org/html/rfc5639#section-3.1
secp256k1 = WeierstrassCurve(
    0,  # a
    7,  # b
    2 ** 256 - 2 ** 32 - 977  # p
)

G = AffinePoint(
    secp256k1,
    # x
    55066263022277343669578718895168534326250603453777594175500187360389116729240,
    # y
    32670510020758816978083085130507043184471273380659243275938904335757337482424,
    2 ** 256 - 432420386565659656852420866394968145599
)

# If we do a scalar multiplication of the generators
# order with the generator point, we should end up
# at the neutral element, the point at infinity
X = G.order * G
assert(X == secp256k1.poif)

# Since the point at infinity is the neutral element,
# with order+1 we should en up at the generator.
X = (G.order + 1) * G
assert(X == G)
