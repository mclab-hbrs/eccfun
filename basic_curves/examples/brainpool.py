from curves import WeierstrassCurve
from curves import AffinePoint

# Take the standardized curve, as here:
# https://tools.ietf.org/html/rfc5639#section-3.1
brainpoolP160r1 = WeierstrassCurve(
    0x340E7BE2A280EB74E2BE61BADA745D97E8F7C300,
    0x1E589A8595423412134FAA2DBDEC95C8D8675E58,
    0xE95E4A5F737059DC60DFC7AD95B3D8139515620F
)

G = AffinePoint(
    brainpoolP160r1,
    0xBED5AF16EA3F6A4F62938C4631EB5AF7BDBCDBC3,
    0x1667CB477A1A8EC338F94741669C976316DA6321,
    0xE95E4A5F737059DC60DF5991D45029409E60FC09
)

# If we do a scalar multiplication of the generators
# order with the generator point, we should end up
# at the neutral element, the point at infinity
X = G.order * G
assert(X == brainpoolP160r1.poif)

# Since the point at infinity is the neutral element,
# with order+1 we should en up at the generator.
X = (G.order + 1) * G
assert(X == G)
