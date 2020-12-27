# -*- coding: utf-8 -


def get_mock_list(page, size):
    # page：分页的第几页
    # size：每页数量

    request = {
        "url": '/mock_server/get_mock_list?page=%s&size=%s' % (page, size),
        "method": "get",
        "headers": {"content-type": "application/json"},
        "data": {}
    }

    return request
