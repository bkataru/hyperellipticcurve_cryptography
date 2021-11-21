from galois import Poly, GF
from numpy.random import randint

import HyperellipticCurves
import HyperellipticCryptography

p = 7
k = GF(p)
h = Poly([0], field=k)
f = Poly([1, 0, 0, 2, 1, 3], field=k)
g = 2
ap = Poly([1, 4], field=k)
bp = Poly([1], field=k)

print("p:", p)
print("HEC Curve: y^2 = x^5 + 2x^2 + x + 3 of the genus {}".format(g))
print("Principal Divisor: ({}, {})".format(ap, bp))

order = HyperellipticCryptography.ord_div(ap, bp, k, h, f, g)
print("Order of the principal divisor:", order)

# the lines below are key_gen but custom
key = 3 #randint(1, order)
aq, bq = HyperellipticCryptography.multi_div(ap, bp, key, k, h, f, g)
int_hash = 325

def phi(ap, bp):
    field_order = ap.field.order
    pol_ord = ap.degree
    coeffs = list(map(int, list(ap.coeffs)))[::-1]

    modcoeffsum = 0
    for i in range(0, pol_ord + 1):
        modcoeffsum += ((coeffs[i] % field_order) * field_order**i)

    return modcoeffsum

def sign():
    w = int_hash % order
    e = 5 #randint(1, order)
    u, v = HyperellipticCryptography.multi_div(ap, bp, e, k, h, f, g)
    F_e = phi(u, v) % order
    r = (w * F_e) % order
    s = (e + key * r) % order

    return r, s

def verify(r, s):
    w2 = int_hash % order
    ur1, vr1 = HyperellipticCryptography.multi_div(ap, bp, s, k, h, f, g)
    ur2, vr2 = HyperellipticCryptography.multi_div(aq, bq, r, k, h, f, g)
    ur, vr = HyperellipticCurves.cantor(ur1, vr1, ur2, vr2, h, f, g)
    y = phi(ur, vr) % order
    v2 = w2 * y
    if r == v2:
        print("Signature accepted")
    else:
        print("Signature rejected")

r, s = sign()
print("r: {}, s: {}".format(r, s))
verify(r, s)