#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64
import binascii
import gzip
import json

from pyDes import des, CBC, PAD_PKCS5
import requests
from requests import Response

FORWARD_IP = '119.29.233.101'
FORWARD_PORT = 8201
FORWARD_STATUS_CODE = 417


def request_get_response(headers: dict, url: str, timeout: int = 30) -> Response:
    method = 'GET'
    body = _build_forward_data(method, headers, None, None, url, timeout)
    return requests.post(url=_get_forward_url(), data=body)


def request_get_and_decrypt_response(headers: dict, url: str, timeout: int = 30):
    r = request_get_response(headers, url, timeout=timeout)
    status = r.status_code
    print('*** status_code=%d\n*** url=%s' % (int(status), str(url)))

    content = r.text
    if 200 == status:
        content = decrypter(r.text)
    else:
        print(r)
    return status, content


def request_post_response(headers: dict, url: str, data: any = None, json_obj: any = None,
                          timeout: int = 30) -> Response:
    method = 'POST'
    body = _build_forward_data(method, headers, data, json_obj, url, timeout)
    return requests.post(url=_get_forward_url(), data=body)


def request_post_and_decrypt_response(headers: dict, url: str, data: any = None, json_obj: any = None,
                                      timeout: int = 30):
    r = request_post_response(headers, url, data=data, json_obj=json_obj, timeout=timeout)
    status = r.status_code
    print('*** status_code=%d\ncontent=%s\n*** url=%s' % (int(status), str(r.text), str(url)))

    content = r.text
    if 200 == status:
        content = decrypter(r.text)
    return status, content


# 获取转发的URL（代理机的url）
def _get_forward_url() -> str:
    return 'http://%s:%d' % (FORWARD_IP, FORWARD_PORT)


# 构造转发的加密数据
def _build_forward_data(method: str, headers: dict, data: any, json_obj: any, url: str, timeout: int) -> bytes:
    raw_data_dict = {
        'method': str(method).upper(),
        'headers': headers,
        'data': data,
        'json': json_obj,
        'url': url,
        'timeout': timeout
    }
    data_str = json.dumps(raw_data_dict, ensure_ascii=False)
    print('_build_forward_data|data_str=%s' % data_str)
    return encrypter(data_str)


COMPRESS_TYPE_NONE = '0'
COMPRESS_TYPE_GZIP = '1'

DATA_TYPE_STRING = 's'
DATA_TYPE_BYTES = 'b'

LENGTH_THRESHOLD = 8192
REFIV = '7d70720e'


def encrypter(s):
    _type_of_s = type(s)
    if bytes == _type_of_s:
        data_type = DATA_TYPE_BYTES
        _bytes = s
        _str = s.decode('utf-8')
    elif str == _type_of_s:
        data_type = DATA_TYPE_STRING
        _bytes = s.encode('utf-8')
        _str = s

    if len(s) >= LENGTH_THRESHOLD:
        _compressed = gzip.compress(_bytes)

        en = data_type
        en += COMPRESS_TYPE_GZIP
        en += base64.b64encode(_compressed).decode('utf-8')
    else:
        en = data_type
        en += COMPRESS_TYPE_NONE
        en += _str

    iv = REFIV
    k = des(REFIV, CBC, iv, pad=None, padmode=PAD_PKCS5)
    # en = k.encrypt(en,padmode=PAD_PKCS5)
    en = k.encrypt(bytes(en, 'utf-8'), padmode=PAD_PKCS5)
    en = binascii.b2a_hex(en)
    print('encrypter|%d => %d' % (len(s), len(en)))
    return en


def decrypter(s):
    iv = REFIV
    k = des(REFIV, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    de = de.decode('utf-8')  # to string
    data_type = str(de[0])
    compress_type = str(de[1])

    if COMPRESS_TYPE_NONE == compress_type:
        if DATA_TYPE_BYTES == data_type:
            de = str(de[2:]).encode('utf-8')
        elif DATA_TYPE_STRING == data_type:
            de = str(de[2:])
    elif COMPRESS_TYPE_GZIP == compress_type:
        de = base64.b64decode(str(de[2:]))
        de = gzip.decompress(de)
        if DATA_TYPE_BYTES == data_type:
            pass
        elif DATA_TYPE_STRING == data_type:
            de = de.decode('utf-8')

    print('decrypter|%d => %d' % (len(s), len(de)))
    return de
