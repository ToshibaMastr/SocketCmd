import time
import socket
from stdThread import StdThread


class BestSocket:
    nconn = 0
    conn = None

    def __init__(self, HOST: int, PORT: str, type: str):
        self.socket = socket.socket()

        if type == 'server':
            self.conns = []
            self._thr = None

            self.socket = socket.socket()
            self.socket.bind((HOST, PORT))
            self.socket.listen(50)
        elif type == 'client':
            self.conn = socket.socket()
            self.socket.connect((HOST, PORT))
            self.conn = _SProtocol(self.socket)

    def send(self, data):
        """Отправляет данные в соединение"""
        self.conn.send(data.encode('cp866'))

    def recv(self) -> bytes:
        """Получает данные из соединения"""
        return self.conn.recv().decode('cp866')

    def recvMsg(self):
        """Получает сообщение из соединения"""
        rawMsg = self.recv()
        return rawMsg[:2], rawMsg[2:]

    def sendFile(self, file: str):
        """Загружает файл через соединение"""
        recived = 0
        with open(file, 'rb') as f:
            while True:
                rawFile = f.read(1024)
                if not rawFile:
                    self.send('00')
                    yield 'Ok!'
                    return
                self.conn.send(rawFile)
                recvcode = self.recv()
                if recvcode != '2017':
                    yield 'Wrong!'
                    return
                recived += 1
                yield str(recived)

    def recvFile(self, file: str):
        """Сохраняет файл через соединение"""
        recived = 0
        with open(file, 'wb') as f:
            while True:
                rFile = self.conn.recv()
                if rFile == b'00':
                    yield 'Ok!'
                    return
                f.write(rFile)
                self.send('2017')
                recived += 1
                yield str(recived)

    def findConns(self) -> list:
        """Находит подключения, возвращает ip подключений"""
        while not self._thr or not self._thr.is_alive():
            if self._thr:
                self.conns.append(_CProtocol(*self._thr.join()))
            time.sleep(0.25)
            self._thr = StdThread(target=self.socket.accept)
            self._thr.start()
        return [conn.info for conn in self.conns]

    def setConn(self, num: int):
        """Устанавливает подключение"""
        self.nconn = num
        self.conn = self.conns[num]

    def delConnection(self):
        del self.conns[self.nconn]


class _CProtocol:
    conn = None

    def __init__(self, conn: socket, info: list):
        conn.send(b'T')
        self.conn = conn
        self.info = info

    def send(self, data):
        """Отправляет данные в соединение"""
        self.conn.send(len(data).to_bytes(4))
        self.conn.send(data)
        time.sleep(0.001)

    def recv(self) -> bytes:
        """Получает данные из соединения"""
        time.sleep(0.001)
        return self.conn.recv(int.from_bytes(self.conn.recv(4)))


class _SProtocol(_CProtocol):
    def __init__(self, conn: socket):
        if conn.recv(1) == b'T':
            self.conn = conn
        else:
            return -1
