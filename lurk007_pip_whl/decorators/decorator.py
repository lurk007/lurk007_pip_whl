# coding:utf-8
import ctypes
import inspect
import os
import threading
import time
from lurk007_pip_whl.config.conf import log_path
from lurk007_pip_whl.os.thread.my_thread import MyThread
from lurk007_pip_whl.time.date import Date

local = threading.Lock()


def thread_pid(func):
    """

    :param func:
    :return: 返回当前线程的pid
    """

    def get(*args, **kwargs):
        res = func(*args, **kwargs)
        pid = ctypes.CDLL('libc.so.6').syscall(186)
        return res, pid

    return get


def daemon_thread(time_out=None, interval=1):
    """
    :param time_out: 最大执行时长
    :param interval: 监听结果间隔时间
    :return:
    """

    def cur1(func):
        def cur2(*args, **kwargs):
            thread = MyThread(target=func, args=args, kwargs=kwargs)
            thread.setDaemon(True)  # 守护线程
            thread.start()
            if time_out:
                nums = range(time_out // interval)
                for i in nums:
                    time.sleep(interval)
                    result = thread.get_result()
                    if result:
                        return result
            else:
                while True:
                    result = thread.get_result()
                    if result:
                        return result
                    else:
                        time.sleep(interval)
            return None

        return cur2

    return cur1


def synchronization(func):
    """
    在函数上方加上synchronization就可以变成同步方法
    :param func:
    :return:
    """

    def lock(*args, **kwargs):
        local.acquire()
        local.locked()
        try:
            res = func(*args, **kwargs)
            return res
        finally:
            local.release()

    return lock


def logger(func):
    caller = inspect.stack()[1][4][0].replace("\n", "")

    def run(*args, **kwargs):
        p = inspect.stack()[1][1].split('/')[-3::]
        s = ''
        index = 0
        for i in p:
            if index == 0:
                index += 1
                continue
            s += F'{i}.'
        s = s.replace('.py', '')
        root_path = log_path
        os.system(F'mkdir {root_path} -p')
        path = F"{root_path}/{s}{caller}.log".replace('def ', '').replace(':', '')
        print('log_path:', path)
        with open(path, 'a') as f:
            f.write(F'[{Date.now()}]\n')
            f.write(F"params:>{*args, *kwargs}\n")
            res = func(*args, **kwargs)
            f.write(F"return:>{res}\n\n")
        return res

    return run


def lissen_time(func):
    def int_time(*args, **kwargs):
        start_time = time.time()  # 程序开始时间
        print("RUN", )
        res = func(*args, **kwargs)
        over_time = time.time()  # 程序结束时间
        total_time = over_time - start_time
        s = int(total_time)
        ms = int(total_time * 1000)
        mss = int(total_time * 1000 * 1000)
        print(F"OVER 程序耗时{s}秒 {ms}毫秒 {mss}微秒")
        return res

    return int_time


def singleton(cls, *args, **kwargs):
    """单例模式"""
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@logger
def main(a, b):
    print(a + b)


if __name__ == '__main__':
    main(1, 2)
    # main(a, b)
