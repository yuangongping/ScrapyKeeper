import threading
import time


class ThreadWithResult(threading.Thread):
    """  带返回数据的线程 """
    def run(self):
        try:
            if self._target:
                self.result = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

    def get_result(self):
        return self.result

#
# def task(name):
#     print('%s start' % name)
#     time.sleep(3)
#     print('%s end' % name)
#     return 'return name %s' % name

# ta = ThreadWithResult(target=task('t1'), args={'name': t1})


# class TreadWithResult(threading.Thread):
#     """  带返回数据的线程 """
#     def __init__(self, func, args=()):
#         super(TreadWithResult, self).__init__()
#         self.func = func
#         self.args = args
#
#     def run(self):
#         self.result = self.func(*self.args)
#
#     def get_result(self):
#         try:
#             return self.result
#         except Exception:
#             return None
