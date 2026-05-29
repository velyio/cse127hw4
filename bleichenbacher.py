from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from roots import *
import sys

# Takes message as a command line argument
message = sys.argv[1]

# Your code to forge a signature goes here.
# Load the public key and extract n and e
pubkey_str = """-----BEGIN PUBLIC KEY-----
          MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAqtMbmgeGOL5l+sylkG5C
          AgAmCmCXmN/KNFuIJaF1cxKMoiZzlqew3DVNF+Xs5rkFkzrflw2MVLY8SQl/qyRO
          yHNy68OVwXeAbSIyY/8reUh2AXTm013HVS+LvI6yVOgQ4AwvfbuAPQ4B+nYbkK9G
          wgHczJrChPMOaZz7yMBBwwEeonqdeNkuAyAsM/E7UmxCsR3FdMF3vuARLY/+7UJx
          wDMFO1LMt5zOrQtK3AKiT4GTv4orBMAZ159ocBawpq6Z5emuI6opGavxLrjTlQgG
          KagUNHhQXnQ/+pX6wPuMzWVv21z6L6m3Fbm/bWpyLteftEO7d+vMS8HTDzFQgjN2
          bwIBAw==
          -----END PUBLIC KEY-----"""
publickey = RSA.importKey(pubkey_str)
n = publickey.n #
e = publickey.e # the exponent, should be 3

# Hash the message using SHA-1
h = SHA.new(message.encode())
digest = h.digest()

# Make the fake padded message
msg = bytearray()
msg.append(0x00)
msg.append(0x01)

# Does not check the number of 0xFF byte
msg.extend(b'\xFF'* 8)
msg.append(0x00)
# ASN.1 "magic" bytes for SHA-1
msg.extend(b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14')
# 20-byte SHA-1 digest
msg.extend(digest)  

# Pad the rest of the message with zeros
msg.extend(b'\x00' * (256 - len(msg)))


padded_message = bytes(msg)

# Take the cube root of the padded message
# turn bytes to integer using function from root.py
m = bytes_to_integer(padded_message)

s, is_exact = integer_nthroot(m, e)

# turn the integer signature back to bytes
print(integer_to_base64(s).decode())

# some example functions from roots
# root, is_exact = integer_nthroot(27, 3)
# print(integer_to_base64(root).decode())