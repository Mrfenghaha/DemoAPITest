# -*- coding: utf-8 -


def configs_info():

    request = {
        "url": "/mock_server/get_configs",
        "method": "get",
        "headers": {"content-type": "application/json"},
        "data": {}
    }

    return request


