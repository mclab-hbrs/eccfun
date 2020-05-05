from curves import WeierstrassCurve

# Toy example to test plotting
subgroup = (
    37,
    (1211, 872),
    [
        (0, 1), (1211, 872), (2176, 1087), (1469, 121), (1545, 2448), (985, 689), (2333, 1830), (888, 1300),
        (1735, 729), (954, 1451), (1686, 2370), (1041, 1930), (949, 1355), (1542, 149), (1960, 2042), (229, 17),
        (1269, 2493), (1537, 2014), (1024, 643), (1024, 1860), (1537, 489), (1269, 10), (229, 2486), (1960, 461),
        (1542, 2354), (949, 1148), (1041, 573), (1686, 133), (954, 1052), (1735, 1774), (888, 1203), (2333, 673),
        (985, 1814), (1545, 55), (1469, 2382), (2176, 1416), (1211, 1631)
    ]
)

lines = []

for i in range(2, len(subgroup[2])):
    lines.append(
        {
            "from": subgroup[2][i-1],
            "to": subgroup[2][i]
        }
    )

p = 2503
toy_curve = WeierstrassCurve(3, 7, p)
toy_curve.plot(lines=lines).show()