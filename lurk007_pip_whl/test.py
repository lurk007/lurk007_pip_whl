from lurk007_pip_whl.db.my_query import MyQuery
from lurk007_pip_whl.db.my_redis import Redis
from lurk007_pip_whl.db.mysql_pool import MysqlPool

if __name__ == '__main__':
    s = "id大于9995 [or]" \
        "d000001小于等于1 [and]" \
        "d000002小于等于1 [and]" \
        "d000003小于等于1 [and]" \
        "d000004小于等于1 [and]" \
        "d000005小于等于1 [and]" \
        "d000006小于等于1 [and]" \
        "d000007小于等于1 [and]" \
        "d000001小于等于1 [and]" \
        "d000002小于等于1 [and]" \
        "d000003小于等于1 [and]" \
        "d000004小于等于1 [and]" \

    operator = ['小于等于', '小于', '大于', '大于等于', '等于', '不等于', '为空', '不为空', 'in', '包含', '不包含', '介于']
    r = Redis
    t = r.get('test')
    li = None
    result = None
    if t:
        li = eval(t)
    else:
        msp = MysqlPool()
        v = msp.fetchall('select * from test')
        r.set('test', str(v))
        t = r.get('test')
        li = eval(t)
    if li:
        pass
        # query = MyQuery(li,operator,s)
        # query.get_result()
