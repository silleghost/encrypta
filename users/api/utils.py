import pyotp

def verify_totp_code(totp_code, totp_secret):
    totp = pyotp.TOTP(totp_secret)
    return totp.verify(totp_code)