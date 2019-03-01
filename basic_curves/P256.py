from curves import WeierstrassCurve
from curves import AffinePoint

p = 2**256 - 2**224 + 2**192 + 2**96 - 1
curveP256 = WeierstrassCurve(-3, 41058363725152142129326129780047268409114441015993725554835256314039467401291, p)

G = AffinePoint(
        curveP256,
        48439561293906451759052585252797914202762949526041747995844080717082404635286,
        36134250956749795798585127919587881956611106672985015071877198253568414405109,
        115792089210356248762697446949407573529996955224135760342422259061068512044369
)

# If we do a scalar multiplication of the generators
# order with the generator point, we should end up
# at the neutral element, the point at infinity
X = G.order * G
assert(X == curveP256.poif)

# Since the point at infinity is the neutral element,
# with order+1 we should en up at the generator.
X = (G.order + 1) * G
assert(X == G)
