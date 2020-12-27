# -*- coding: utf-8 -


def operations_show_lists(page, size):
    # page：分页的第几页
    # size：每页数量

    request = {
        "url": '/db_operation/get_operation_list?page=%s&size=%s' % (page, size),
        "method": "get",
        "headers": {"content-type": "application/json"},
        "data": {}
    }

    return request
