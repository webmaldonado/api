import base64
from resources.SystemConfig import ClsSystemConfig


def set_header():
    configs = ClsSystemConfig.get('f282375a9c5f4f849e2716d39bf1d627')
    if configs.API_NeedSendCredentials == False:
        return {'Content-Type': 'application/json'}

    password_decode_bytes = configs.API_Password.encode('ascii')
    password_decode = base64.decodebytes(password_decode_bytes)
    password_string = password_decode.decode("utf-8")

    credentials = f'{configs.API_User}:{password_string}'
    credentials_bytes = credentials.encode('ascii')
    base64_bytes = base64.b64encode(credentials_bytes)
    credentials_base64 = base64_bytes.decode('ascii')

    return {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {credentials_base64}'
    }