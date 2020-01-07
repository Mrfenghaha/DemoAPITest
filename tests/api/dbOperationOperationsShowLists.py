# -*- coding: utf-8 -


def operations_show_lists(page_num, num):
    # page_num：分页的第几页
    # num：每页数量

    request = {
        "url": '/db_operation/operations/show_lists',
        "method": "post",
        "headers": {"content-type": "application/json"},
        "data": {"page_num": page_num, "num": num}
    }

    return request
