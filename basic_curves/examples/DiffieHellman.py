from curves import WeierstrassCurve
from curves import AffinePoint
import random
# Now we can do a simple Elliptic Curve Diffie Hellman
# Key Exchange

# These values are standardized and known to every one
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

print("Curve is: ", brainpoolP160r1)
print("Generator is: ", G)

# Alice's side
# Create Secret Key
alice_secret = random.randint(2, G.order)
# Create public key that we can send over
# untrustworthy channel
alice_public = alice_secret * G
print("Alice's public key is: ", alice_public)

# Bob's side
bob_secret = random.randint(2, G.order)
bob_public = bob_secret * G
print("Bob's public key is: ", bob_public)

# Agree on shared secret
# Alice's side
alice_shared_secret = alice_secret * bob_public

# Bob's side
bob_shared_secret = bob_secret * alice_public

assert(alice_shared_secret == bob_shared_secret)
print("Agreed upon secret is: ", alice_shared_secret)
