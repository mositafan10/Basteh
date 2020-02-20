
import kavenegar
import random

def generate_otp():
    return ''.join(str(random.randint(0,9)) for _ in range(5))

def set_otp(phone, otp):
    model_name = "otp"
    key = '%s_%s_%s' % ( model_name,phone,otp)
    if not cache.get(key):
        cache.set(key,True)
    send_sms(phone, otp)

def send_sms(phone_number, otp):
    text="Your verification code is: {}".format(otp)

def verify_otp(phone, otp):
    model_name = "otp"
    key = '%s_%s_%s' % ( model_name,phone,otp)
    if cache.get(key) == otp:
        #login
        return
    else:
        raise Exception()

    