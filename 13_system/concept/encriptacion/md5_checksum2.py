"""
From https://www.youtube.com/watch?v=M0wqrfKiSNA

>>>import hashlib

>>>hashlib.algorithms_guaranteed
A set containing the names of the hash algorithms guaranteed to be supported by
this module on all platforms.
{'sha3_224', 'sha224', 'sha3_384', 'sha256', 'blake2s', 'sha3_256', 'sha3_512', 
'shake_128', 'blake2b', 'shake_256', 'sha512', 'sha384', 'sha1', 'md5'}
"""
import hashlib

# These methods return the encoded
# string in hexadecimal format
print("Hexadecimal format")
print(hashlib.md5(b"Carlos Lacaci Moya").hexdigest())
print(hashlib.sha1(b"Carlos Lacaci Moya").hexdigest())
print(hashlib.sha512(b"Carlos Lacaci Moya").hexdigest())
print("_________________________")

print("Byte format")
# These two returns the encoded data in byte format
print(hashlib.md5(b"Carlos Lacaci Moya").digest())
print(hashlib.sha1(b"Carlos Lacaci Moya").digest())
print(hashlib.sha512(b"Carlos Lacaci Moya").digest())
