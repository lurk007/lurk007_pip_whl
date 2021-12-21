# 我用的版本是3.5.1
from croniter import croniter
from datetime import datetime


class MyCron(object):
    def __init__(self):
        self.str_time_now = datetime.now()
        pass

    def cron_iter(self, fmt, count=None):
        try:
            itrs = croniter(fmt, self.str_time_now)
        except Exception as e:
            print(e)
            raise RuntimeError("语法错误")
        time_lapses = None
        date = None
        if count:
            time_lapses = [itrs.get_next() for _ in range(count)]
            date = [str(itrs.get_next(datetime)) for _ in range(count)]
        return itrs, time_lapses, date


if __name__ == '__main__':
    # '*  *  *  *  *  *'
    #  '分 时 日 月 周 秒'
    cron = MyCron()
    itr, time_lape, dates = cron.cron_iter('0-20 0-8/2 1 * * 0', 10)
    print(time_lape)
    for i in dates:
        print(i)
