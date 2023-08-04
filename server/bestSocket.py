import time
import socket
from stdThread import *

class BestSocket():
    conns = []
    conn = None
    _thr = None

    def __init__(self, HOST:int, PORT:str, type:str):
        self.conn = socket.socket()
        if type=='server':
            self.conn.bind((HOST, PORT))
            self.conn.listen(50)
            #self.conn, addr = self.conn.accept()
        elif type=='client':
            self.conn.connect((HOST, PORT))

    def sendFile(self, file:str):
        """Загружает файл через соединение"""
        with open(file, 'rb') as f:
            while True:
                rawFile = f.read(1024)
                if not rawFile:
                    break
                self.send(rawFile)
            self.send(b'00')

    def recvFile(self, file:str):
        """Сохраняет файл через соединение"""
        with open(file, 'wb') as f:
            while True:
                rFile = self.recv()
                if rFile==b'00':
                    break
                f.write(rFile) 

    def send(self, data):
        """Отправляет данные в соединение"""
        self.conn.send(len(data).to_bytes(4))
        self.conn.send(data)
        time.sleep(0.01)

    def recv(self) -> bytes:
        """Получает данные из соединения"""
        time.sleep(0.01)
        return self.conn.recv(int.from_bytes(self.conn.recv(4)))

    def recvMsg(self):
        """Получает сообщение из соединения"""
        rawMsg = self.recv()
        return rawMsg[:2], rawMsg[2:]

    def findConns(self) -> list:
        """Находит подключения, возвращает ip подключений"""
        while not self._thr or not self._thr.is_alive():
            if self._thr:
                self.conns.append(self._thr.join())
            self._thr = StdThread(target=self.conn.accept)
            self._thr.start()
            time.sleep(0.5)
        return [conn[1] for conn in self.conns]

    def setConn(self, num:int):
        """Устанавливает подключение"""
        self.conn = self.conns[num][0]

    def closeConns(self):
        """Закрывает подключения"""
        for conn in self.conns:
            conn.close()#+
    
    def close(self):
        """Закрывает подключение"""
        self.conn.close()