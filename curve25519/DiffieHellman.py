from Curve25519 import Curve25519
import random
# Alice's side
# Create Secret Key
alice_secret = random.randint(2, 2**255-19)
# Create public key that we can send over
# untrustworthy channel
alice = Curve25519(alice_secret)
print("Alice's public key is: ", alice.pk)

# Bob's side
# Create Secret Key
bob_secret = random.randint(2, 2**255-19)
# Create public key that we can send over
# untrustworthy channel
bob = Curve25519(bob_secret)
print("Bob's public key is: ", bob.pk)

# Agree on shared secret
# Alice's side
alice_shared_secret = alice.compute_shared(bob.pk)

# Bob's side
bob_shared_secret = bob.compute_shared(alice.pk)

assert(alice_shared_secret == bob_shared_secret)
print("Agreed upon secret is: ", alice_shared_secret)
