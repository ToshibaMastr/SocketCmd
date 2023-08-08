from bestSocket import *
from bCCmd import *

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
            ast = bc.read()
            if ast[0] == 47:
                asp = argsSplit(ast[1:])
                match asp[0].lower():
                    case b'lfile':
                        bs.send(b'/lfile ' + asp[2])
                        bs.sendFile(asp[1])

                    case b'sfile':
                        bs.send(b'/sfile ' + asp[2])
                        bs.recvFile(asp[1])

                    case b'setconn':
                        bs.setConn(int(asp[1]))
                        bc.connectTo(*conns[int(asp[1])], int(asp[1]))

                    case b'findconn':
                        bc.findConns()
                        conns = bs.findConns()
                        bc.connections(conns)

                    case _:
                        bc.error(f'Unknown command : /{str(asp[0], encoding="cp866")}\n')

                bs.send(b'/N')
            else:
                bs.send(ast+b'\n')