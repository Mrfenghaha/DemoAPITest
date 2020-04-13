# -*- coding: utf-8 -
from features.apis import mockServerMockShowLists_api


def suite_post(data):
    page_num, num = data['page_num'], data['num']

    # 发起登录
    login = mockServerMockShowLists_api.mock_show_lists(page_num, num)
    return login
