class command:
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

class help(command):
    name = 'help'
    info = '._.'
    inputs = [['command', 'Команда.']]
    def use(self, bc, bs, args):
        if len(args) == 1:
            for command in commands.values():
                command._about(bc)
            bc.newLine()
        elif len(args) == 2:
            try:
                commands[args[1]]._help(bc)
            except KeyError:
                bc.error(f'Команда {args[1]} не найдена.\n')

class lfile(command):
    name = 'lfile'
    info = 'Копирует файл с сервера на клиент.'
    inputs = [['file', 'Копируемый файл на сервере.'], ['newFile', 'Новый файл у клиента.']]
    def use(self, bc, bs, args):
        if len(args)==len(self.inputs)+1:
            bc.info(f'Копирую файл (server){args[1]} на (client){args[2]}.\n')
            bs.send(b'/lfile ' + args[2].encode('cp866') + b'\n')
            for ans in bs.sendFile(args[1]):
                match ans:
                    case 'Ok!':
                        bc.info(f'Успешно!.\n')
                        break
                    case 'Wrong':
                        bc.error(f'Что-то пошло не так...\n')
                        break
                    case _:
                        bc.info(f'{ans}kb' + '\n')
        else:
            bc.error(f'Неверный синтаксис команды.\n')

class sfile(command):
    name = 'sfile'
    info = 'Копирует файл с клиента на сервер.'
    inputs = [['file', 'Копируемый файл клиента.'], ['newFile', 'Новый файл на сервере.']]
    def use(self, bc, bs, args):
        if len(args)==len(self.inputs)+1:
            bc.info(f'Копирую файл (client){args[1]} на (server){args[2]}.\n')
            bs.send(b'/sfile ' + args[1].encode('cp866') + b'\n')
            if(not bs.recvFile(args[2])):
                bc.error(f'Что-то пошло не так...\n')
            else:
                bc.info(f'Успешно!.\n')
        else:
            bc.error(f'Неверный синтаксис команды.\n')

class findconn(command):
    name = 'findconn'
    info = 'Поиск и подключение новых клиентов.'
    inputs = []
    def use(self, bc, bs, args):
        if len(args)==len(self.inputs)+1:
            bc.info(f'Поиск.\n')
            conns = bs.findConns()
            bc.connections(conns)
        else:
            bc.error(f'Неверный синтаксис команды.\n')

class setconn(command):
    name = 'setconn'
    info = 'Соединение с клиентом.'
    inputs = [['num', 'Номер клиента.']]
    def use(self, bc, bs, args):
        if len(args)==len(self.inputs)+1:
            bc.info(f'Соединение.\n')
            conns = bs.findConns()
            bc.connections(conns)
        else:
            bc.error(f'Неверный синтаксис команды.\n')

commands = {'help':help(), 'lfile':lfile(), 'sfile':sfile(), 'findconn':findconn(), 'setconn':setconn()}