# -*- coding: utf-8 -


def demo_post(page_num, num):
    # page_num：分页的第几页
    # num：每页数量

    request = {
        "url": '/mock_server/mock/show_lists',
        "method": "post",
        "headers": {"content-type": "application/json"},
        "data": {"page_num": page_num, "num": num}
    }

    return request
