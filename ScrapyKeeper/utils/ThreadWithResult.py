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

