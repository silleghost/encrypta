import base64
import random
import hashlib
import hmac
import time
import struct

# def verify_totp_code2(totp_code, totp_secret):
#     totp = pyotp.TOTP(totp_secret)
#     return totp.verify(totp_code)

def generate_secret_key(length=32):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    return "".join(random.choice(chars) for _ in range(length))

    
def verify_totp_code(totp_code, totp_secret):
    key = base64.b32decode(totp_secret)
    current_time = int(time.time() / 30)

    for i in range(-1, 1):
        counter = struct.pack(">Q", current_time + i)
        hmac_hash = hmac.new(key, counter, hashlib.sha1).digest()
        offset = hmac_hash[-1] & 0x0F
        truncatedHash = hmac_hash[offset:offset + 4]
        code = struct.unpack(">L", truncatedHash)[0] & 0x7FFFFFFF
        code %= 1000000
        if str(totp_code) == str(code):
            return True
    
    return False
