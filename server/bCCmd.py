class BCCmd:
    def read(self) -> bytes:
        """Чтение команды."""
        data = input('\033[1m')
        print('', end='\033[0m')
        return data

    def write(self, string: bytes):
        """Вывод текста из CMD."""
        print(string, end='')

    def findConns(self):
        """Поиск подключений."""
        print('\033[92m' + '○ Finding connections...', end='\033[0m\n')

    def connections(self, conns: list):
        """Вывод всех соединений."""
        st = '\033[92m→\033[32m connections \033[92m'
        for conn in conns:
            st += f'{conn[0]}:{str(conn[1])}, '
        else:
            st = st[:-2]
        print(st, end='\n\033[0m')

    def connectTo(self, host: str, port: int, num: int):
        """Вывод 'соединения к клиенту'."""
        print(f'\033[92m↓\033[32m Connect to \033[92m{host}:{port} ({num})\033[0m')

    def newLine(self, lines=1):
        """Переход на следующую строку"""
        print('\n'*(lines-1))

    def error(self, err):
        """Отображение ошибки."""
        if type(err) == bytes:
            err = str(err, encoding='cp866')
        print('\033[91m' + err, end='\033[0m')

    def info(self, err):
        """Отображение информацию."""
        if type(err) == bytes:
            err = str(err, encoding='cp866')
        print('\033[93m' + err, end='\033[0m')
