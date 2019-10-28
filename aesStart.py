#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from base64 import b64encode,b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad

def run():
    data = b"secret123456abcda"
    print ("The message was: ", data)
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC,iv)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))

    result = json.dumps({'iv':b64encode(iv),'key':b64encode(key),'data':b64encode(data),'ciphertext':b64encode(ct_bytes)});

    print result

    b64 = json.loads(result)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("The message was: ", pt)

    input()

if __name__ == '__main__':
    run()
