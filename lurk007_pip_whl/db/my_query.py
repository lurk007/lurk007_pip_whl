class MyQuery(object):
    """
    精准查询类
    """

    def __init__(self, keys, values, operator1, operator2):
        self.keys = keys
        self.values = values
        self.operator1 = operator1
        self.operator2 = operator2

    def get_result(self):
        pass

    @staticmethod
    def gt(li, key, v):
        """
        大于
        """
        for i in li:
            if i[key] > v:
                yield i

    @staticmethod
    def gtq(li, key, v):
        """
        大于等于
        """
        for i in li:
            if i[key] >= v:
                yield i

    @staticmethod
    def lt(li, key, v):
        """
        小于
        小于

        """
        for i in li:
            if i[key] < v:
                yield i

    @staticmethod
    def ltq(li, key, v):
        """
        小于等于
        """
        for i in li:
            if i[key] <= v:
                yield i

    @staticmethod
    def eq(li, key, v):
        """
        等于
        """
        for i in li:
            if i[key] == v:
                yield i

    @staticmethod
    def neq(li, key, v):
        """
        不等于
        """
        for i in li:
            if i[key] != v:
                yield i

    @staticmethod
    def none(li, key, v):
        """
        为空
        """
        for i in li:
            if i[key] is None or i[key] == '':
                yield i

    @staticmethod
    def not_none(li, key, v):
        """
        不为空
        """
        for i in li:
            if i[key] is not None and i[key] != '':
                yield i

    @staticmethod
    def is_in(li, key, v):
        """
        in
        """
        for i in li:
            if i[key] in v:
                yield i

    @staticmethod
    def included(li, key, v):
        """
        包含
        """
        for i in li:
            if v in i[key]:
                yield i

    @staticmethod
    def not_included(li, key, v):
        """
         不包含
        """
        for i in li:
            if v not in i[key]:
                yield i

    @staticmethod
    def between(li, key, v):
        """
        介于
        """
        for i in li:
            if i[key] == v:
                yield i


operator_mapping = {
    '大于': MyQuery.gt,
    '小于': MyQuery.lt,
    '大于等于': MyQuery.gtq,
    '小于等于': MyQuery.ltq,
    '等于': MyQuery.eq,
    '不等于': MyQuery.neq,
    '为空': MyQuery.none,
    '不为空': MyQuery.not_none,
    'in': MyQuery.is_in,
    '介于': MyQuery.between,
    '包含': MyQuery.included,
    '不包含': MyQuery.not_included,
}
