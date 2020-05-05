from curves import WeierstrassCurve
from curves import EdwardsCurve
from curves import MontgommeryCurve

# Toy examples to test plotting
p = 61
toy_curve = WeierstrassCurve(-1, 0, p)
toy_curve.plot().show()

toy_ed = EdwardsCurve(123, 2503)
toy_ed.plot().show()

toy_mn = MontgommeryCurve(123, 7, 2503)
toy_mn.plot().show()
