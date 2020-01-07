# -*- coding: utf-8 -


def configs_info():

    request = {
        "url": "/mock_server/configs/info",
        "method": "get",
        "headers": {"content-type": "application/json"},
        "data": {}
    }

    return request


