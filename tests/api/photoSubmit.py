# -*- coding: utf-8 -
from config.readConfig import *
from common.runMain import RunMain
from urllib3 import encode_multipart_formdata


def photo_submit(token):

    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'docs')

    files = {'upload': ('image.png', open(os.path.join(path, '400k.png'), 'rb').read(), 'multipart/form-data')}
    encode_data = encode_multipart_formdata(files)

    url = host + '/api/photo_submit'
    method = 'post_file'
    headers = {'content-type': encode_data[1], 'token': token}
    data = encode_data[0]

    result = RunMain(method, url, headers, data).run_main()
    return result
