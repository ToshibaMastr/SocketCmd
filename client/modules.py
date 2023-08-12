class _command:
    def use(self):
        pass


class _lfile(_command):
    def use(self, _, bs, args):
        if len(args) == 1:
            for i in bs.recvFile(args[0]):
                if i == 'Ok!' or i == 'Wrong!':
                    break


class _sfile(_command):
    def use(self, _, bs, args):
        if len(args) == 1:
            for i in bs.sendFile(args[0]):
                if i == 'Ok!' or i == 'Wrong!':
                    break


_commands = {'sfile': _sfile(),
             'lfile': _lfile()}


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
    print(args)
    return args


def execute(commandLine: list, bc, bs):
    """Исполняет команду."""
    args = argsSplit(commandLine)
    if args[0] in _commands:
        _commands[args[0]].use(bc, bs, args[1:])
