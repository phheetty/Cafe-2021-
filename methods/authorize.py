from datetime import datetime
import base64
import os, sys
import random
import string
'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'

def debug_row(e):
    exc_type, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno, e)
    return exc_type, fname, exc_tb.tb_lineno, e

def generate_authorize(taxid):
    try:
        if len(taxid) <= 5:
            return {"status":"ER","message":"taxid error"}
        auth_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        data = str(auth_time) + "_" + str(taxid)
        encode = auth_encode(data)
        return {"status":"OK","message":encode}
    except Exception as e:
        message = debug_row(e)
        result = {"status":"ER","message":message}
        return result

def check_authorization_timeout(Authorization, Taxid=""):
    try:
        Auth_decode = auth_decode(Authorization)
        if type(Auth_decode) == dict:
            result = Auth_decode
            return result
        data = Auth_decode.split('_')
        if len(data) != 2:
            result = {"status": "ER", "message": "Bad authorization"}
            return result
        Auth_decode = {
                "Taxid": data[1],
                "Auth_time": data[0]
            }
        now = datetime.now()
        now_dtm = now.strftime("%Y%m%d%H%M%S")
        date_auth = (datetime.strptime(Auth_decode['Auth_time'],"%Y-%m-%dT%H:%M:%S")).strftime("%Y%m%d%H%M%S")
        if (int(now_dtm) - int(date_auth)) > 100:
            result = {"status": "ER", "message": "Your authorization timeout"}
            return result
        if Auth_decode['Taxid'] != Taxid:
            result = {"status":"ER","message":"Your authorization not match with taxid"}
            return result
        result = {"status": "OK","message":"Authorize Valid"}
    except Exception as e:
        message = debug_row(e)
        result = {"status": "ER","message":"Token Error"}
    finally:
        return result


def auth_encode(data):
    try:
        letters = string.ascii_lowercase
        front = ''.join(random.choice(letters) for i in range(50))
        back = ''.join(random.choice(letters) for i in range(35))
        # auth_enc = base64.b64encode(bytes(data, 'utf-8'))
        # auth_enc = auth_enc.decode('utf-8')
        # result = auth_enc

        auth_enc = base64.b64encode(bytes(data, 'utf-8'))
        auth_enc = auth_enc.decode('utf-8')
        keys = front + auth_enc + back
        result = keys
    except Exception as e:
        message = debug_row(e)
        result = {"status": "ER", "message": message}
    return result

def auth_decode(data):
    try:
        # auth_dec = jwt.decode(data,'bill',algorithms='HS256')
        data = data[50:-35]
        auth_dec = base64.b64decode(bytes(data, 'utf-8'))
        result = auth_dec.decode('utf-8')
    except Exception as e:
        message = debug_row(e)
        result = {"status": "ER", "message": message}
    return result


