# -*- coding: utf-8 -
from config.readConfig import *


def photo_submit(token):
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'docs')

    request = {
        "url": host + '/api/photo_submit',
        "method": 'post_file',
        "headers": {'token': token},
        "data": {'upload': ('image.png', open(os.path.join(path, '400k.png'), 'rb').read(), 'multipart/form-data')}
    }

    return request
