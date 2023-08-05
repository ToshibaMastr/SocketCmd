class BCCmd:
    def read(self) -> bytes:
        """Чтение команды"""
        data = input('\033[1m').encode('cp866')
        print('', end='\033[0m')
        return data
    
    def write(self, string:bytes):
        """Вывод текста из CMD"""
        print(str(string, encoding='cp866'), end='')
    
    def findConns(self):
        """Поиск подключений"""
        print('\033[92m' + '○ Finding connections...', end = '\033[0m\n')

    def connections(self, conns:list):
        """Вывод всех соединений"""
        st = '\033[92m' + '→ connections '
        for conn in conns:
            st += f'{conn[0]}:{str(conn[1])}, '
        else:
            st = st[:-2]
        print(st, end = '\n\033[0m')

    def connectTo(self, host:str, port:int, num:int):
        """Вывод 'соединения к порту'"""
        print('\033[92m' + f'↓ Connect to {host}:{port} ({num})', end = '\033[0m\n')
    
    def newLine(self, lines=1):
        """Переход на следующую строку"""
        print('\n'*(lines-1))
    
    def error(self, err):
        """Отображение ошибки"""
        if type(err)==bytes:
            err = str(err, encoding='cp866')
        print('\033[91m' + err, end = '\033[0m')

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
