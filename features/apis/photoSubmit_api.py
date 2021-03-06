# -*- coding: utf-8 -
import os


def photo_submit(token):
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'docs')

    request = {
        "url": "/apis/photo_submit",
        "method": "post_file",
        "headers": {"token": token},
        "data": {"upload": ("image.png", open(os.path.join(path, "file.png"), "rb").read(), "multipart/form-data")}
    }

    return request
