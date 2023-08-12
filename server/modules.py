class _command:
    name = ''
    info = ''
    inputs = []

    def use(self):
        pass

    def _about(self, bc):
        bc.info(f'/{self.name}: {self.info}\n')

    def _help(self, bc):
        out = f'{self.info}\n/{self.name}'
        for i in self.inputs:
            out += f' [{i[0]}]'
        for i in self.inputs:
            out += f'\n: {i[0]} - {i[1]}'
        out += '\n'*2
        bc.info(out)


class _help(_command):
    name = 'help'
    info = '._.'
    inputs = [['command', 'Команда.']]

    def use(self, bc, bs, args, nl):
        if len(args) == 0:
            for command in _commands.values():
                command._about(bc)
        elif len(args) == 1:
            try:
                _commands[args[0]]._help(bc)
            except KeyError:
                bc.error(f'Команда {args[0]} не найдена.\n')
        if nl:
            bs.send('\n')


class _findconn(_command):
    name = 'findconn'
    info = 'Поиск и подключение новых клиентов.'
    inputs = []

    def use(self, bc, bs, args, nl):
        bc.findConns()
        conns = []
        while conns == []:
            conns = bs.findConns()
        bc.connections(conns)
        if nl:
            bs.send('\n')


class _setconn(_command):
    name = 'setconn'
    info = 'Соединение с клиентом.'
    inputs = [['num', 'Номер клиента.']]

    def use(self, bc, bs, args, nl):
        num = int(args[0])
        bs.setConn(num)
        bc.connectTo(*bs.conns[num].info, num)
        if nl:
            bs.send('\n')


class _lfile(_command):
    name = 'lfile'
    info = 'Копирует файл с сервера на клиент.'
    inputs = [['file', 'Копируемый файл на сервере.'],
              ['newFile', 'Новый файл у клиента.']]

    def use(self, bc, bs, args, nl):
        bc.info(f'Копирую файл (server){args[0]} на (client){args[1]}.\n')
        bs.send('/lfile ' + args[1])
        recived = 0
        with open(args[0], 'rb') as f:
            while True:
                rawFile = f.read(1024)
                if not rawFile:
                    bs.send('00')
                    bc.info('Успешно!.\n')
                    break
                bs.conn.send(rawFile)
                recvcode = bs.recv()
                if recvcode != '2017':
                    bc.error('Что-то пошло не так...\n')
                    break
                recived += 1
                bc.info(f'{recived}kb' + '\n')


class _sfile(_command):
    name = 'sfile'
    info = 'Копирует файл с клиента на сервер.'
    inputs = [['file', 'Копируемый файл клиента.'],
              ['newFile', 'Новый файл на сервере.']]

    def use(self, bc, bs, args, nl):
        bc.info(f'Копирую файл (client){args[0]} на (server){args[1]}.\n')
        bs.send('/sfile ' + args[0])

        recived = 0
        with open(args[1], 'wb') as f:
            while True:
                rFile = bs.conn.recv()
                if rFile == b'00':
                    bc.info('Успешно!.\n')
                    break
                f.write(rFile)
                bs.send('2017')
                recived += 1
                bc.info(f'{recived}kb' + '\n')


_commands = {
    'help': _help(),
    'lfile': _lfile(),
    'sfile': _sfile(),
    'findconn': _findconn(),
    'setconn': _setconn()
}


def argsSplit(commandLine: str) -> list:
    """Преобразует строку в массив."""
    s, arg = True, ''
    args = []
    for i in commandLine:
        if s and i == ' ':
            args.append(arg)
            arg = ''
        elif i == '"':
            s = not s
        else:
            arg += i
    args.append(arg)
    return args


def execute(commandLine: list, bc, bs, nl=False):
    """Исполняет команду."""
    args = argsSplit(commandLine)
    if not args[0] in _commands:
        bc.error(f'Команда /{args[0]} не найдена, используйте /help для'
                 ' получения полного списка команд.\n')
        if nl:
            bs.send('\n')
        return
    comm = _commands[args[0]]
    if not len(comm.inputs) == len(args)-1:
        bc.error('Неверный синтаксис команды.\n')
        if nl:
            bs.send('\n')
        return
    comm.use(bc, bs, args[1:], nl)
