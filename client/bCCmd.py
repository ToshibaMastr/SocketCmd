from subprocess import PIPE, Popen, CREATE_NO_WINDOW
import time
from stdThread import *

CLUSTER_SIZE = 128
class BCCmd:
    def __init__(self):
        self.process = Popen("cmd /T:f0", stdin=PIPE, stdout=PIPE, stderr=PIPE, creationflags = CREATE_NO_WINDOW)
        self.threadOut = StdThread(target=self.process.stdout.read, args=(1, ))
        self.threadErr = StdThread(target=self.process.stderr.read, args=(1, ))
        
        self.threadOut.start()
        self.threadErr.start()
        
        time.sleep(2.017)
        
    def send(self, c:str):
        self.process.stdin.write(c + b'\n')
    
    def flush(self):
        self.process.stdin.flush()
        time.sleep(1)

    def kill(self):
        """Убивает CMD."""
        self.process.kill()

    def stdall(self, std:str, func, tp:str=b'', prefix=b'') -> (bytes):
        """Возвращяет текст из потока."""
        thread, process = (self.threadOut, self.process.stdout) if std=='out' else (self.threadErr, self.process.stderr)
        claster = b''
        
        while not thread.is_alive():
            text, thread = self._stdall(process, thread, CLUSTER_SIZE-len(claster))
            claster += text
            if len(claster)==CLUSTER_SIZE:
                func(tp + claster.removeprefix(prefix[:CLUSTER_SIZE]))
                prefix = prefix[CLUSTER_SIZE:]
                claster = b''
            time.sleep(0.1)
        if claster:
            func(tp + claster.removeprefix(prefix[:CLUSTER_SIZE]))
        
        if std=='out':
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
            #time.sleep(0.001)
        return text, thread

def argsSplit(c:str) -> list:
    """Преобразует строку в массив"""
    s, j = True, b''
    args = []
    for i in c:
        if s and i==32:
            args.append(j)
            j=b''
        elif i==34:
            s = not s
        else:
            j += i.to_bytes()
    args.append(j)
    return args