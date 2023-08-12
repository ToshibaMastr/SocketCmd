class _command:
    def use(self):
        pass


class _lfile(_command):
    def use(self, bc, bs, args):
        if len(args) == 1:
            with open(args[0], 'wb') as f:
                while True:
                    rFile = bs.conn.recv()
                    if rFile == b'00':
                        break
                    f.write(rFile)
                    bs.send('2017')


class _sfile(_command):
    def use(self, bc, bs, args):
        if len(args) == 1:
            with open(args[0], 'rb') as f:
                while True:
                    rawFile = f.read(1024)
                    if not rawFile:
                        bs.send('00')
                        break
                    bs.conn.send(rawFile)
                    recvcode = bs.recv()
                    if recvcode != '2017':
                        break


_commands = {
    'sfile': _sfile(),
    'lfile': _lfile()
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


def execute(commandLine: list, bc, bs):
    """Исполняет команду."""
    args = argsSplit(commandLine)
    if args[0] in _commands:
        _commands[args[0]].use(bc, bs, args[1:])
