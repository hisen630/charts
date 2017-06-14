# coding:utf-8
"""
    SQL工具集合
"""
from utils import to_iter


class Where():
    def __init__(self, field):
        self.field = field

    def in_(self, items=()):
        """ 接受一个可迭代对象 有元素或无元素  
            1. 有元素且超出1个  IN （x,y,.......）
            2. 只有一个元素     = x
            3. 无元素          "" # 空字符
            
            
            "SELECT * FROM TABLE WHERE id {}".format(in_(id))
        """
        if not items:
            return ""
        items = to_iter(items)

        if len(items) == 1:
            return " {} = {}".format(self.field, items[0])
        return " {} IN ({})".format(self.field, ",".join(map(repr, items)))

    @staticmethod
    def limit(start=0, end=None):

        return " LIMIT {},{}".format(start, end)

    @staticmethod
    def count():
        return " COUNT(1) "

    def like(self, format):
        """ 格式化内容 
            like
        """
        return ''' {} LIKE "{}"'''.format(self.field, format)

    def order_by(self, asc=True):
        asc = "ASC" if asc else "DESC"
        return " ORDER BY {} {} ".format(self.field, asc)

    @staticmethod
    def group_by(*fields):
        return " GROUP BY {}".format(",".join(fields))


class Sql:
    pass


if __name__ == '__main__':
    print Where("name").like("%test%")
