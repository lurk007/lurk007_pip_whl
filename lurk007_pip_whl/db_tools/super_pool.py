# import importlib
# from dbutils.pooled_db import PooledDB
#
from utils_for_lurk007.logger.decorator import log


#
#
# class DataBase(object):
#
#     def __init__(self, db_type, config):
#
#         self.__db_type = db_type
#
#         if self.__db_type == 'mysql':
#             db_creator = importlib.import_module('pymysql')
#         elif self.__db_type == 'sqlserver':
#             db_creator = importlib.import_module('pymssql')
#         elif self.__db_type == 'oracle':
#             db_creator = importlib.import_module('cx_Oracle')
#         else:
#             raise Exception('unsupported database type ' + self.__db_type)
#         self.pool = PooledDB(
#             creator=db_creator,
#             mincached=0,
#             maxcached=6,
#             maxconnections=0,
#             blocking=True,
#             ping=0,
#             **config
#         )
#
#     def execute_query(self, sql, as_dict=True):
#         """ 查询语句 :param sql: :param as_dict: :return: """
#         conn = None
#         cur = None
#         try:
#             conn = self.pool.connection()
#             cur = conn.cursor()
#             cur.execute(sql)
#             rst = cur.fetchall()
#             if rst:
#                 if as_dict:
#                     fields = [tup[0] for tup in cur._cursor.description]
#                     return [dict(zip(fields, row)) for row in rst]
#                 return rst
#             return rst
#
#         except Exception as e:
#             print('sql:[{}]meet error'.format(sql))
#             print(e.args[-1])
#             return ()
#         finally:
#             if conn:
#                 conn.close()
#             if cur:
#                 cur.close()
#
#     def execute_manay(self, sql, data):
#         """ 执行多条语句 :param sql: :param data: :return: """
#         conn = None
#         cur = None
#         try:
#             conn = self.pool.connection()
#             cur = conn.cursor()
#             cur.executemany(sql, data)
#             conn.commit()
#             return True
#         except Exception as e:
#             print('[{}]meet error'.format(sql))
#             print(e.args[-1])
#             conn.rollback()
#             return False
#         finally:
#             if conn:
#                 conn.close()
#             if cur:
#                 cur.close()
#
#
# MySQL = DataBase(
#     'mysql', {'user': 'sa', 'host': '127.0.0.1', 'password': 'xxxx', 'database': 'test', 'port': 3306}
# )
# MsSQL = DataBase(
#     'sqlserver', {'user': 'sa', 'host': '127.0.0.1', 'password': 'xxxxx', 'database': 'test', 'port': 1433}
# )
# Oracle = DataBase(
#     'oracle', {'user': 'sa', 'dsn': '127.0.0.1:1903/google', 'password': 'xxxxxx', 'encoding': 'utf-8'}
# )
@log
def test():
    print('test')


if __name__ == '__main__':
    test()
