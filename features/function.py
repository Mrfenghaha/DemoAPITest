# -*- coding: utf-8 -
import base64


class CustomFunc:

    # 公共方法
    def b64encode(self, value):
        return base64.b64encode(value.encode())

    def b64decode(self, value):
        return base64.b64encode(value.encode())


if __name__ == '__main__':
    pass
