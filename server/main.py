from bestSocket import *
from bCCmd import *
from modules import *

#Toshiba - лучшая компания, ToshibaMastru - хороший человек)
print('\033[0m  ______\033[90m____  _____ __  __________  ___ \033[0m   _ _\n /_  __/\033[90m __ \/ ___// / / /  _/ __ )/   |\033[0m  / V \\\n  / /\033[90m / / / /\__ \/ /_/ // // __  / /| |\033[0m  | \033[90mM\033[0m |\n / /\033[90m / /_/ /___/ / __  // // /_/ / ___ |\033[0m  \\   /\n/_/\033[90m  \____//____/_/ /_/___/_____/_/  |_|\033[0m   \\_/\n')

URL = '127.0.0.1'
PORT = 9090

bs = BestSocket(URL, PORT, 'server')
bc = BCCmd()

bc.findConns()
conns = []
while conns == []:
    conns = bs.findConns()
bc.connections(conns)

bs.setConn(0)
bc.connectTo(*conns[0], 0)

bc.newLine()

while True:
    tp, text = bs.recvMsg()
    match tp:
        case b'|O':
            bc.write(text)
        case b'|E':
            bc.error(text)
        case b'_ ':
            com = bc.read()
            if com and com[0] == 47:
                args = argsSplit(com[1:])

                if args[0] in commands:
                    commands[args[0]].use(bc, bs, args)
                else:
                    bc.error(f'Команда /{args[0]} не найдена, используйте /help для получения полного списка команд.\n')
                bs.send(b'\n')
            else:
                bs.send(com+b'\n')