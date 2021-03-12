# -*- coding: utf-8 -
from databases.delete import *


class DBOperation:
    def delete(self, id):
        result = delete(id)
        return result

