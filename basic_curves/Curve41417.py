from curves import AffinePoint
from curves import EdwardsCurve

# Curve41417 is an edwards curve
# https://safecurves.cr.yp.to/equation.html
Curve41417 = EdwardsCurve(123, 2503)

Curve41417.plot().show()

# We can find its base point online
# https://safecurves.cr.yp.to/base.html
G = AffinePoint(
    Curve41417,
    # x coordinate
    0x1a334905141443300218c0631c326e5fcd46369f44c03ec7f57ff35498a4ab4d6d6ba111301a73faa8537c64c4fd3812f3cbc595,
    # y coordinateq
    0x22,
    # order
    0x7ffffffffffffffffffffffffffffffffffffffffffffffffffeb3cc92414cf706022b36f1c0338ad63cf181b0e71a5e106af79
)
assert(Curve41417.is_on_curve(G))
assert((G.order+1) * G == G)
