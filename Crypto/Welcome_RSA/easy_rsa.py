#!/usr/bin/python3

from Crypto.Util.number import getPrime
from Crypto.Util.number import bytes_to_long

N = 1024
p = getPrime(N)
q = getPrime(N)

m = 0
with open('flag.txt', 'rb') as f:
    m = bytes_to_long(f.read())
e = 65537

phi = (p-1) * (q-1)
c_p = pow(m, e, p)
c_q = pow(m, e, q)

print(f"c_p = {c_p}")
print(f"c_q = {c_q}")
print(f"N = {p * q}")
print(f"phi = {phi}")