# -*- coding: utf-8 -
from data.dbOperation.delete import *


class DBOperation:
    def delete(self, id):
        result = delete(id)
        return result

