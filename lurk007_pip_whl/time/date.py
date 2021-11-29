import time


class Date(object):
    @staticmethod
    def now():
        """
        获取当前时间
        :return: str
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def timestamp(t=None):
        """
        获取当前时间
        :t: 当前时间
        :return: str
        """
        if t:
            timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
            timeStamp = time.mktime(timeArray)
        else:
            timeStamp = time.time()
        return int(timeStamp)


if __name__ == '__main__':
    print(Date.timestamp())
