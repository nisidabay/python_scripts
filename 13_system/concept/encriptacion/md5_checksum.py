"""
From https://www.youtube.com/watch?v=G_Pj1GMe8ro
"""

import hashlib

# This two lines output the same result
# The hash function only takes a sequence of bytes
# as a parameter, thas why the encoding an the
# prepend b"

print(hashlib.md5("Carlos Lacaci Moya".encode("UTF-8")).hexdigest())

print(hashlib.md5(b"Carlos Lacaci Moya").hexdigest())
