import time
import socket
from stdThread import *

class BestSocket():
    conns = []
    conn = None
    _thr = None

    def __init__(self, HOST:int, PORT:str, type:str):
        if type=='server':
            self.socket = socket.socket()
            self.socket.bind((HOST, PORT))
            self.socket.listen(50)
        elif type=='client':
            self.conn = socket.socket()
            while True:
                try:
                    self.conn.connect((HOST, PORT))
                    if self.conn.recv(1)==b'T':
                        break
                except:
                    pass

    def sendFile(self, file:str):
        """Загружает файл через соединение"""
        recived = 0
        with open(file, 'rb') as f:
            while True:
                rawFile = f.read(1024)
                if not rawFile:
                    self.send(b'00')
                    yield 'Ok!'
                self.send(rawFile)
                if self.recv()!=b'2017':
                    yield 'Wrong!'
                recived+=1
                yield str(recived)

    def recvFile(self, file:str):
        """Сохраняет файл через соединение"""
        recived = 0
        with open(file, 'wb') as f:
            while True:
                rFile = self.recv()
                if rFile==b'00':
                    yield 'Ok!'
                f.write(rFile)
                self.send(b'2017')
                recived+=1
                yield str(recived)

    def send(self, data):
        """Отправляет данные в соединение"""
        self.conn.send(len(data).to_bytes(4))
        self.conn.send(data)
        time.sleep(0.001)

    def recv(self) -> bytes:
        """Получает данные из соединения"""
        time.sleep(0.001)
        return self.conn.recv(int.from_bytes(self.conn.recv(4)))

    def recvMsg(self):
        """Получает сообщение из соединения"""
        rawMsg = self.recv()
        return rawMsg[:2], rawMsg[2:]

    def findConns(self) -> list:
        """Находит подключения, возвращает ip подключений"""
        while not self._thr or not self._thr.is_alive():
            if self._thr:
                newConn = self._thr.join()
                newConn[0].send(b'T')
                self.conns.append(newConn)
            time.sleep(0.5)
            self._thr = StdThread(target=self.socket.accept)
            self._thr.start()
        return [conn[1] for conn in self.conns]

    def setConn(self, num:int):
        """Устанавливает подключение"""
        self.conn = self.conns[num][0]

    def closeConns(self):
        """Закрывает подключения"""
        for conn in self.conns:
            conn.close()
    
    def close(self):
        """Закрывает подключение"""
        self.conn.close()