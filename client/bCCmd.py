from subprocess import PIPE, Popen, CREATE_NO_WINDOW
import time
from stdThread import StdThread


CLUSTER_SIZE = 128


class BCCmd:
    def __init__(self):
        self.process = Popen("cmd /T:f0", stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags=CREATE_NO_WINDOW)
        self.threadOut = StdThread(target=self.process.stdout.read, args=(1, ))
        self.threadErr = StdThread(target=self.process.stderr.read, args=(1, ))

        self.threadOut.start()
        self.threadErr.start()

        time.sleep(2.017)

    def send(self, c: str):
        self.process.stdin.write(c.encode('cp866'))

    def flush(self):
        self.process.stdin.flush()
        time.sleep(0.1)

    def kill(self):
        """Убивает CMD."""
        self.process.kill()

    def stdall(self, std: str, func, tp: str = b'', prefix=b'') -> (bytes):
        """Возвращяет текст из потока."""
        thread, process = (self.threadOut, self.process.stdout) if std == 'out' else (self.threadErr, self.process.stderr)
        claster = b''
        while not thread.is_alive():
            text, thread = self._stdall(process, thread, CLUSTER_SIZE-len(claster))
            claster += text
            if len(claster) == CLUSTER_SIZE:
                func(tp + claster.removeprefix(prefix[:CLUSTER_SIZE]))
                prefix = prefix[CLUSTER_SIZE:]
                claster = b''
            time.sleep(0.05)
        if claster:
            func(tp + claster.removeprefix(prefix[:CLUSTER_SIZE]))

        if std == 'out':
            self.threadOut = thread
        else:
            self.threadErr = thread

    def _stdall(self, process, thread, clasterSize=128) -> (bytes):
        text = b''
        for i in range(clasterSize):
            if thread.is_alive():
                break
            text = text + thread.join()
            thread = StdThread(target=process.read, args=(1, ))
            thread.start()
        return text, thread
