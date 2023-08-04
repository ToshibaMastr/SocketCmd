from threading import Thread

class StdThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=()):
        Thread.__init__(self, group, target, name, args, daemon=True)
        self._return = None

    def run(self):
        self._return = self._target(*self._args, **self._kwargs)
                
    def join(self, *args):
        Thread.join(self, *args)
        return self._return