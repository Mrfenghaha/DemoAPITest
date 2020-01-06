# -*- coding: utf-8 -


def demo_get():

    request = {
        "url": "/mock_server/configs/info",
        "method": "get",
        "headers": {"content-type": "application/json"},
        "data": {}
    }

    return request


