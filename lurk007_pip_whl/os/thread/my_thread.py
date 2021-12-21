import ctypes
import inspect
import threading


class MyThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super(MyThread, self).__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        if kwargs is None:
            kwargs = {}
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self.result = None

    def run(self):
        try:
            if self._target:
                self.result = self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
        # 在执行函数的同时，把结果赋值给result,
        # 然后通过get_result函数获取返回的结果  

    def get_result(self):
        """

        :return:
        """
        try:
            return self.result
        except Exception as e:
            return None

    @staticmethod
    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        try:
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                # """if it returns a number greater than one, you're in trouble,
                # and you should call it again with exc=NULL to revert the effect"""
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
        except ValueError as e:
            # print("ValueError>>>", e)
            pass
        except SystemError as e:
            print("SystemError>>>", e)
            pass

    @staticmethod
    def stop(thread):
        """停止线程"""
        MyThread._async_raise(thread.ident, SystemExit)


if __name__ == '__main__':
    pass
