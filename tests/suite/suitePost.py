# -*- coding: utf-8 -
from tests.api import mockServerMockShowLists


def suite_post(data):
    page_num, num = data['page_num'], data['num']

    # 发起登录
    login = mockServerMockShowLists.mock_show_lists(page_num, num)
    return login
