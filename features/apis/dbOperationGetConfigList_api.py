# -*- coding: utf-8 -


def get_configs_list(page, size):
    # page：分页的第几页
    # size：每页数量

    request = {
        "url": '/db_operation/get_config_list?page=%s&size=%s' % (page, size),
        "method": "get",
        "headers": {"content-type": "application/json"},
        "data": {}
    }

    return request
