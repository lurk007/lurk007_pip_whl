import pymysql

log_path = "/home/lurk/my_github/lurk007_pip_whl/logs"
db_pools = [
    {
        'creator': pymysql,  # 使用链接数据库的模块
        'maxconnections': 6,  # 连接池允许的最大连接数，0和None表示不限制连接数
        'mincached': 2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        'maxcached': 5,  # 链接池中最多闲置的链接，0和None不限制
        'maxshared': 3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        'blocking': True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        'maxusage': None,  # 一个链接最多被重复使用的次数，None表示无限制
        'setsession': [],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        'ping': 0,
        # ping MySQL服务端，检查是否服务可用。# 如：0 : None : never, 1 : default : whenever it is requested, 2 : when a cursor is created, 4 : when a query is executed, 7 : always
        'host': '10.34.8.89',
        'port': 3306,
        'user': 'root',
        'password': 'Daqian#123',
        'database': 'jiangxin',
        'charset': 'utf8'
    },
    {
        'creator': pymysql,  # 使用链接数据库的模块
        'maxconnections': 6,  # 连接池允许的最大连接数，0和None表示不限制连接数
        'mincached': 2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        'maxcached': 5,  # 链接池中最多闲置的链接，0和None不限制
        'maxshared': 3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        'blocking': True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        'maxusage': None,  # 一个链接最多被重复使用的次数，None表示无限制
        'setsession': [],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        'ping': 0,
        # ping MySQL服务端，检查是否服务可用。# 如：0 : None : never, 1 : default : whenever it is requested, 2 : when a cursor is created, 4 : when a query is executed, 7 : always
        'host': '192.168.3.102',
        'port': 3306,
        'user': 'root',
        'password': '123123',
        'database': 'jiangxin102',
        'charset': 'utf8'
    },
    {
        'creator': pymysql,  # 使用链接数据库的模块
        'maxconnections': 6,  # 连接池允许的最大连接数，0和None表示不限制连接数
        'mincached': 2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        'maxcached': 5,  # 链接池中最多闲置的链接，0和None不限制
        'maxshared': 3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        'blocking': True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        'maxusage': None,  # 一个链接最多被重复使用的次数，None表示无限制
        'setsession': [],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        'ping': 0,
        # ping MySQL服务端，检查是否服务可用。# 如：0 : None : never, 1 : default : whenever it is requested, 2 : when a cursor is created, 4 : when a query is executed, 7 : always
        'host': '192.168.3.221',
        'port': 3306,
        'user': 'root',
        'password': '123123',
        'database': 'jiangxin',
        'charset': 'utf8'
    },
]
redis_confs = [
    {
        'host': '192.168.3.234',
        'port': 6377,
        'db': 0,
        'password': '123456',
        'socket_timeout': None,
        'socket_connect_timeout': None,
        'socket_keepalive': None,
        'socket_keepalive_options': None,
        'connection_pool': None,
        'unix_socket_path': None,
        'encoding': 'utf-8',
        'encoding_errors': 'strict',
        'charset': None,
        'errors': None,
        'decode_responses': False,
        'retry_on_timeout': False,
        'ssl': False,
        'ssl_keyfile': None,
        'ssl_certfile': None,
        'ssl_cert_reqs': 'required',
        'ssl_ca_certs': None,
        'ssl_check_hostname': False,
        'max_connections': None,
        'single_connection_client': False,
        'health_check_interval': 0,
        'client_name': None,
        'username': None,
        'retry': None
    }
]
db_pool = db_pools[1]
redis_conf = redis_confs[0]
