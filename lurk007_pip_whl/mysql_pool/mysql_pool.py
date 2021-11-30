import pymysql
from dbutils.pooled_db import PooledDB
from lurk007_pip_whl.config.conf import db_pool

'''
同步连接池
'''


class MysqlPool(object):
    def __init__(self):
        self.POOL = PooledDB(
            creator=db_pool["creator"],  # 使用链接数据库的模块
            maxconnections=db_pool["maxconnections"],  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=db_pool["mincached"],  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=db_pool["maxcached"],  # 链接池中最多闲置的链接，0和None不限制
            maxshared=db_pool["maxshared"],
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=db_pool["blocking"],  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=db_pool["maxusage"],  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=db_pool["setsession"],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=db_pool["ping"],
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=db_pool['host'],
            port=db_pool['port'],
            user=db_pool['user'],
            password=db_pool['password'],
            database=db_pool['database'],
            charset=db_pool['charset'],
        )

    def __new__(cls, *args, **kw):
        '''
        启用单例模式
        :param args:
        :param kw:
        :return:
        '''
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(self):
        '''
        启动连接
        :return:
        '''
        conn = self.POOL.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    def close(self, conn, cursor):
        '''
        关闭连接
        :param conn:
        :param cursor:
        :return:
        '''
        cursor.close()
        conn.close()

    def fetchall(self, sql, args=None, count=0):
        '''
        批量查询
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.connect()

        cursor.execute(sql, args)
        if count <= 0:
            record_list = cursor.fetchall()
        else:
            record_list = self.__fetch(cursor, count)
        self.close(conn, cursor)

        return record_list

    def fetchone(self, sql, args=None):
        '''
        查询单条数据
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.connect()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.close(conn, cursor)

        return result

    def execute(self, sql, args=None):
        '''
        插入数据
        :param sql:
        :param args:
        :return:
        '''
        conn, cursor = self.connect()
        row = cursor.execute(sql, args)
        conn.commit()
        self.close(conn, cursor)
        return row

    def is_existence(self, table_name):
        result = self.fetchone(" SHOW TABLES LIKE %s", (table_name,))
        return result

    def desc(self, table_name):
        result = self.fetchone("SELECT DATABASE() as db_name", None)
        if result is None:
            return None
        else:
            db_name = result['db_name']
            print(db_name)
            result = self.fetchone(
                "select * from information_schema.columns where table_schema = %s and table_name = %s",
                (db_name, table_name,))
        return result

    def while_do(self, target, cursor, args=(), kwargs=None, count=0):
        """
        对每一条数据作任意操作
        """
        if kwargs is None:
            kwargs = {}
        result = list()
        if count == 0:
            while True:
                res = cursor.fetchone()
                if res:
                    result.append(target(res, *args, **kwargs))
                else:
                    break
        else:
            nums = range(count)
            for i in nums:
                res = cursor.fetchone()
                if res:
                    result.append(target(res, *args, **kwargs))
                else:
                    break
        return result

    def __fetch(self, cursor, count):
        nums = range(count)
        result = list()
        for i in nums:
            res = cursor.fetchone()
            if res:
                result.append(res)
            else:
                break
        return result


def test(res, a, b, c):
    print(res)
    print(a)
    print(b)
    print(c)
    return res['id']


if __name__ == '__main__':
    pass
    msp = MysqlPool()
    print(msp.fetchall("select * from daqian_role_menu", count=3))
    # result = msp.while_do(target=test, cursor=cursor, args=(1, 2, 3,))
    # print(result)
