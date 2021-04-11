import hashlib

def set_md5(str):
    res = hashlib.md5()
    res.update(str.encode('utf-8'))
    return res.hexdigest()