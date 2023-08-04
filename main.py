from bestSocket import *
from bCCmd import *

URL = ''
PORT = 9090

bs = BestSocket(URL, PORT, 'server')
bc = BCCmd()

conns = []
while conns == []:
    conns = bs.findConns()
bc.connections(conns)

bs.setConn(0)
bc.connectTo(*conns[0], 0)

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
                        conns = bs.findConns()
                        bc.connections(conns)

                    case _:
                        bc.error(f'Unknown command : /{str(asp[0], encoding="cp866")}')

                bs.send(b'/N')
            else:
                bs.send(ast)